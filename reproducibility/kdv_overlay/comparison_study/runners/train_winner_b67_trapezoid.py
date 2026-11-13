#!/usr/bin/env python3
"""Fresh KdV-B winner 67 with corrected conservation quadrature. Reference diagnostics never affect optimization or stopping."""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import random
import time

import numpy as np
from scipy.io import loadmat
import torch

ROOT = Path(__file__).resolve().parents[2]
CASE = dict(case_id='test_01', amplitude_1=1., frequency_1=1,
            amplitude_2=0., frequency_2=0)
PAPER_L2 = 4.27e-4
MODEL_SHA = '94ce8f7fa29dbb035192bad0efa65f841db89884cf408d456b21433337a60d2a'
PROVENANCE = ROOT / 'comparison_study/provenance/kdv_b_winner_067_trapezoid'
REFERENCE_SHA = '0df03aee69597c8913f7120324303f663db617be3789b9ff35beb29303b1c087'


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dump(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)


def cpu_tree(obj):
    if isinstance(obj, torch.Tensor):
        return obj.detach().cpu().clone()
    if isinstance(obj, dict):
        return {k: cpu_tree(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [cpu_tree(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(cpu_tree(v) for v in obj)
    return obj


def schedule(completed, target):
    fraction = min(completed / target, 1.)
    scale = .05 + .95 * min(fraction / .35, 1.)
    phase = max(0., (fraction - .35) / .65)
    lr = 1.15e-3 if fraction < .35 else 1e-7 + .5 * (1.15e-3 - 1e-7) * (1 + math.cos(math.pi * phase))
    return scale, lr


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--minutes', type=float, default=None, help='Optional cumulative run-loop cap; default: no wall-clock limit')
    p.add_argument('--max-steps', type=int, default=200000)
    p.add_argument('--eval-every', type=int, default=1000)
    p.add_argument('--checkpoint-every', type=int, default=5000)
    p.add_argument('--batch-size', type=int, default=4096)
    p.add_argument('--seed', type=int, default=99417)
    p.add_argument('--threads', type=int, default=4)
    p.add_argument('--device', choices=['auto', 'mps', 'cuda', 'cpu'], default='auto')
    p.add_argument('--output', type=Path, default=ROOT / 'comparison_study/outputs/winner_b067_trapezoid_200k')
    p.add_argument('--resume', action='store_true')
    a = p.parse_args()
    if (a.minutes is not None and a.minutes <= 0) or min(a.max_steps, a.eval_every, a.checkpoint_every, a.batch_size, a.threads) <= 0:
        p.error('Budgets, intervals, batch size and threads must be positive')
    out = a.output.resolve()
    # Reject existing runs before doing any training; resume is explicit.
    if not a.resume and out.exists() and any(out.iterdir()):
        p.error('Output is not empty; use --resume or a new --output')
    out.mkdir(parents=True, exist_ok=True)
    lock = out / 'RUNNING.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        p.error('RUNNING.lock exists. Check no process is running before removing a stale lock.')
    os.write(fd, str(os.getpid()).encode()); os.close(fd)
    try:
        run(a, out)
    finally:
        lock.unlink(missing_ok=True)


def run(a, out):
    source = PROVENANCE / 'candidate.py'
    refpath = ROOT / 'protected_evaluation/data/kdv.mat'
    for path, expected in [(source, MODEL_SHA), (refpath, REFERENCE_SHA)]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Source/reference hash mismatch: {path}')
    if a.device == 'auto':
        a.device = 'cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu')
    device = torch.device(a.device)
    torch.set_num_threads(a.threads)
    random.seed(a.seed); np.random.seed(a.seed); torch.manual_seed(a.seed)
    candidate = load_module(source, 'frozen_b067')
    model = candidate.build_model(CASE).to(device)
    # Reuse the exact original PDE and IC implementations, not a rewritten residual.
    protocol_path = PROVENANCE / 'experiment.py'
    selection = json.loads((PROVENANCE / 'final_selection.json').read_text())
    assert hashlib.sha256(protocol_path.read_bytes()).hexdigest() == selection['protocol']['experiment_sha256']
    protocol = load_module(protocol_path, 'kdv_b_protocol')
    stream = protocol.TrainingBatchStream(device, a.seed + 101, a.batch_size)
    opt = candidate.SOAPAdEMAMix(model.parameters(), lr=candidate.LEARNING_RATE,
        betas=(.9, .99, .999), alpha=0., eps=1e-8, weight_decay=0., precondition_frequency=80)
    data = loadmat(refpath)
    t, x, ref = data['t'].ravel(), data['x'].ravel(), data['usol'].astype(np.float64)
    if ref.shape != (201, 512) or ref.shape != (len(t), len(x)):
        raise ValueError('Unexpected reference grid')
    x_ic = torch.tensor(x, dtype=torch.float32, device=device).reshape(-1, 1)
    config = dict(selected_trial=67, variant="trapezoidal conservation quadrature",
                  parent_candidate_sha256="82cb2913d504de2b8c347e84f6e71574d5479255d22998f7024df5bb730872ef", model_parameters=sum(p.numel() for p in model.parameters()),
                  optimizer='frozen SOAPAdEMAMix; frequency=80; eps=1e-8; zero weight decay',
                  invariant_weight=.1, invariant_slices=8, invariant_spatial_points=512, case=CASE, pde='u_t + u*u_x + 0.022^2*u_xxx = 0',
                  periodic_derivatives=[0, 1, 2], max_steps=a.max_steps,
                  budget_seconds=None if a.minutes is None else a.minutes * 60, eval_every=a.eval_every,
                  checkpoint_every=a.checkpoint_every, batch_size=a.batch_size,
                  seed=a.seed, device=str(device), model_sha256=MODEL_SHA,
                  reference_sha256=REFERENCE_SHA, paper_relative_l2=PAPER_L2,
                  schedule='step fraction of max_steps; 35% domain expansion and alpha warmup, then 65% cosine LR decay',
                  timing='elapsed run loop includes diagnostics/checkpoints; setup and finalization excluded',
                  protocol_sha256=hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
                  torch_version=torch.__version__)
    step, previous_seconds, first, history = 0, 0., None, []
    if a.resume:
        old = json.loads((out / 'config.json').read_text())
        if old != config:
            raise ValueError('Resume requires the same configuration/device; no schedule or budget changes')
        state = torch.load(out / 'latest.pt', map_location='cpu', weights_only=False)
        model.load_state_dict(state['state_dict']); opt.load_state_dict(state['optimizer_state'])
        step, previous_seconds, first, history = state['step'], state['elapsed_seconds'], state['first_below_paper'], state['history']
        torch.set_rng_state(state['torch_rng']); random.setstate(state['python_rng'])
        np.random.set_state(state['numpy_rng']); stream.generator.set_state(state['batch_rng'])
        stream.count = state['batch_count']
        if 'mps_rng' in state: torch.mps.set_rng_state(state['mps_rng'])
        if 'cuda_rng' in state: torch.cuda.set_rng_state_all(state['cuda_rng'])
    else:
        dump(out / 'config.json', config)
        (out / 'frozen_candidate.py').write_bytes(source.read_bytes())
    x_grid = torch.linspace(-1., 1., candidate.INV_POINTS, device=device).reshape(-1, 1)
    exact_energy = CASE['amplitude_1']**2 + CASE['amplitude_2']**2
    started = time.monotonic()
    elapsed = lambda: previous_seconds + time.monotonic() - started

    def budget_exhausted():
        return config['budget_seconds'] is not None and elapsed() >= config['budget_seconds']

    def save(name):
        state = dict(step=step, elapsed_seconds=elapsed(), state_dict=cpu_tree(model.state_dict()),
                     optimizer_state=cpu_tree(opt.state_dict()), torch_rng=torch.get_rng_state(),
                     python_rng=random.getstate(), numpy_rng=np.random.get_state(),
                     batch_rng=stream.generator.get_state(), batch_count=stream.count,
                     first_below_paper=first, history=history, config=config)
        if device.type == 'mps': state['mps_rng'] = torch.mps.get_rng_state()
        if device.type == 'cuda': state['cuda_rng'] = torch.cuda.get_rng_state_all()
        target = out / name; tmp = target.with_suffix('.tmp')
        torch.save(state, tmp); tmp.replace(target)

    def evaluate(final=False):
        nonlocal first
        model.eval(); parts = []
        with torch.no_grad():
            for start in range(0, ref.size, 4096):
                ix = np.arange(start, min(start + 4096, ref.size))
                tx = np.column_stack([t[ix // len(x)], x[ix % len(x)]])
                parts.append(model(torch.tensor(tx, dtype=torch.float32, device=device)).cpu().numpy().ravel())
        pred = np.concatenate(parts).reshape(ref.shape).astype(np.float64)
        err = pred - ref
        row = dict(step=step, elapsed_seconds=elapsed(), relative_l2=float(np.linalg.norm(err) / np.linalg.norm(ref)),
                   rmse=float(np.sqrt(np.mean(err**2))), max_abs_error=float(np.max(np.abs(err))),
                   alpha=float(model.alpha.detach().cpu()))
        if not np.isfinite(list(row.values())).all(): raise FloatingPointError('Nonfinite evaluation')
        if not history or history[-1]['step'] != step:
            history.append(row)
        with (out / 'reference_error_history.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys()); writer.writeheader(); writer.writerows(history)
        if row['relative_l2'] < PAPER_L2 and first is None:
            first = dict(**row, paper_relative_l2=PAPER_L2,
                         meaning='first evaluated checkpoint below threshold; crossing between checks is unknown',
                         previous_evaluated_step=history[-2]['step'] if len(history) > 1 else None)
            dump(out / 'first_below_paper.json', first)
            save('first_below_paper.pt')
            np.savez_compressed(out / 'first_below_paper_predictions.npz', t=t, x=x, u_pred=pred, u_ref=ref)
            print('FIRST OBSERVED BELOW PAPER:', json.dumps(first), flush=True)
        dump(out / 'live_status.json', dict(status='finalizing' if final else 'training', **row))
        if final:
            np.savez_compressed(out / 'prediction_reference.npz', t=t, x=x, u_pred=pred, u_ref=ref)
        print('REFERENCE', json.dumps(row), flush=True)
        save('latest.pt')
        model.train()
        return row

    reason = 'unknown'
    try:
        if not history and not budget_exhausted(): evaluate()
        while step < a.max_steps and not budget_exhausted():
            scale, lr = schedule(step, a.max_steps)
            for group in opt.param_groups:
                group['lr'] = lr
                group['alpha'] = 2. * min(step / (.35 * a.max_steps), 1.)
            tx = stream.next()
            tx = torch.cat([tx[:, :1] * scale, tx[:, 1:]], dim=1)
            opt.zero_grad(set_to_none=True)
            ph, ic = protocol.physics_components(model, tx, CASE, x_ic)
            # Only method change: matching trapezoidal quadrature on the same grid.
            slices = torch.rand((candidate.INV_SLICES, 1), device=device) * scale
            inv_tx = torch.cat([slices.repeat_interleave(candidate.INV_POINTS, dim=0),
                                x_grid.repeat(candidate.INV_SLICES, 1)], dim=1)
            u_inv = model(inv_tx).view(candidate.INV_SLICES, candidate.INV_POINTS)
            mass, energy = candidate.conservation_losses(u_inv, x_grid, exact_energy)
            loss = ph + candidate.IC_WEIGHT * ic + candidate.INV_WEIGHT * (mass + energy)
            if not bool(torch.isfinite(loss)): raise FloatingPointError('Nonfinite training loss')
            loss.backward()
            if budget_exhausted(): break
            opt.step(); step += 1
            if step == 1 or step % 100 == 0:
                status = dict(status='training', step=step, elapsed_seconds=elapsed(),
                              loss=float(loss.detach()), pde_loss=float(ph.detach()), invariant_mass=float(mass.detach()),
                              invariant_energy=float(energy.detach()), lr=lr, optimizer_alpha=opt.param_groups[0]['alpha'],
                              time_domain_upper=scale)
                dump(out / 'live_status.json', status)
                with (out / 'training_history.jsonl').open('a') as f:
                    f.write(json.dumps(status) + '\n')
                print('TRAIN', json.dumps(status), flush=True)
            if step % a.eval_every == 0: evaluate()
            if step % a.checkpoint_every == 0:
                save(f'step_{step:07d}.pt'); save('latest.pt')
        reason = 'max_steps' if step >= a.max_steps else 'time_budget'
    except KeyboardInterrupt:
        reason = 'keyboard_interrupt'
    except BaseException as error:
        save('latest.pt')
        dump(out / 'live_status.json', dict(status='failed', step=step, error=repr(error)))
        raise
    # No optimizer updates occur beyond either configured limit. Final scoring/saving can exceed the clock cap.
    loop_seconds = elapsed()
    metrics = evaluate(final=True)
    save('latest.pt'); save('final.pt')
    dump(out / 'summary.json', dict(status='complete' if reason != 'keyboard_interrupt' else 'interrupted',
         stop_reason=reason, step=step, loop_elapsed_seconds=loop_seconds,
         finalization_elapsed_seconds=elapsed(), final_metrics=metrics, first_below_paper=first))
    print('STOP', reason, 'steps', step, flush=True)


if __name__ == '__main__':
    main()
