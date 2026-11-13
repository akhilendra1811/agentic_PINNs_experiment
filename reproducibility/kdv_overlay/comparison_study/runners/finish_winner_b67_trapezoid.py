"""Independently audit a completed KdV-B winner long run and export scientific figures."""
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'kdv-mpl-cache'))
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import loadmat
import torch
import train_winner_b67_trapezoid as runner

ROOT = runner.ROOT
OUT = ROOT / 'comparison_study/outputs/winner_b067_trapezoid_200k'
PAPER = runner.PAPER_L2


def read_csv(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)


def main(out=None, console=None):
    global OUT
    if out is not None:
        OUT = Path(out).resolve()
    summary = json.loads((OUT / 'summary.json').read_text())
    assert summary['status'] == 'complete'
    config = json.loads((OUT / 'config.json').read_text())
    state = torch.load(OUT / 'final.pt', map_location='cpu', weights_only=False)
    assert state['step'] == summary['step'] <= config['max_steps']
    counters = {int(s['step']) for s in state['optimizer_state']['state'].values()}
    assert counters == {state['step']}, counters
    source = OUT / 'frozen_candidate.py'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == runner.MODEL_SHA
    reference_path = ROOT / 'protected_evaluation/data/kdv.mat'
    assert hashlib.sha256(reference_path.read_bytes()).hexdigest() == runner.REFERENCE_SHA
    refdata = loadmat(reference_path)
    data = np.load(OUT / 'prediction_reference.npz')
    t, x, ref, pred = [data[k] for k in ['t', 'x', 'u_ref', 'u_pred']]
    assert np.array_equal(t, refdata['t'].ravel()) and np.array_equal(x, refdata['x'].ravel())
    assert np.array_equal(ref, refdata['usol'])
    error = pred.astype(np.float64) - ref.astype(np.float64)
    # Separate sum-of-squares implementation from the runner's norm reduction.
    rel = float(np.sqrt(np.sum(error ** 2, dtype=np.float64) / np.sum(ref ** 2, dtype=np.float64)))
    rmse = float(np.sqrt(np.mean(error ** 2, dtype=np.float64)))
    assert abs(rel - summary['final_metrics']['relative_l2']) < 1e-14
    assert abs(rmse - summary['final_metrics']['rmse']) < 1e-14
    torch.set_num_threads(4)
    model = runner.load_module(source, 'audited_b067').build_model(runner.CASE).eval()
    model.load_state_dict(state['state_dict'])

    def predict():
        chunks = []
        with torch.no_grad():
            for start in range(0, ref.size, 4096):
                ix = np.arange(start, min(start + 4096, ref.size))
                tx = np.column_stack([t[ix // len(x)], x[ix % len(x)]])
                chunks.append(model(torch.tensor(tx, dtype=torch.float32)).numpy().ravel())
        return np.concatenate(chunks).reshape(ref.shape).astype(np.float64)

    cpu_pred = predict()
    max_difference = float(np.max(np.abs(cpu_pred - pred)))
    assert max_difference < 1e-4, max_difference
    cpu_l2 = float(np.sqrt(np.sum((cpu_pred - ref)**2) / np.sum(ref**2)))
    protocol = runner.load_module(runner.PROVENANCE / 'experiment.py', 'audit_protocol')
    validation = protocol.validate(model, runner.CASE, t, x, torch.device('cpu'))
    history = read_csv(OUT / 'reference_error_history.csv')
    below = [r for r in history if float(r['relative_l2']) < PAPER]
    assert bool(below) == bool(summary['first_below_paper'])
    audit = dict(step=state['step'], optimizer_step_counters=sorted(counters),
                 relative_l2=rel, rmse=rmse, max_abs_error=float(np.max(np.abs(error))),
                 cpu_reload_relative_l2=cpu_l2, cpu_vs_saved_prediction_max_abs_difference=max_difference,
                 reference_grid_points=int(ref.size), model_parameters=sum(p.numel() for p in model.parameters()),
                 validation_cpu=validation, below_paper_observed=bool(below), paper_relative_l2=PAPER,
                 candidate_sha256=runner.MODEL_SHA, reference_sha256=runner.REFERENCE_SHA)
    runner.dump(OUT / 'independent_verification.json', audit)
    # Offline saved-checkpoint scoring independently reconstructs progress from weights.
    snapshot_rows = []
    for ckpt in sorted(OUT.glob('step_*.pt')):
        s = torch.load(ckpt, map_location='cpu', weights_only=False)
        model.load_state_dict(s['state_dict']); cp = predict(); err = cp - ref
        snapshot_rows.append(dict(step=s['step'], relative_l2_cpu=float(np.sqrt(np.sum(err**2)/np.sum(ref**2))),
                                  rmse_cpu=float(np.sqrt(np.mean(err**2)))))
    write_csv(OUT / 'checkpoint_errors_cpu.csv', snapshot_rows)
    print('Audit:', json.dumps(audit), flush=True)

    plt.rcParams.update({'font.size':9, 'axes.spines.top':False, 'axes.spines.right':False, 'pdf.fonttype':42})
    images = OUT / 'figures'; images.mkdir(exist_ok=True)

    def export(fig, name):
        fig.savefig(images / (name + '.png'), dpi=200, bbox_inches='tight')
        fig.savefig(images / (name + '.pdf'), bbox_inches='tight')
        plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=(12, 6), layout='constrained')
    for ax, field, label in zip(axes[0], [ref, pred, np.abs(error)], ['Numerical reference', 'B67 corrected quadrature: 200,000 steps', 'Absolute error']):
        kw = dict(vmin=ref.min(), vmax=ref.max()) if label != 'Absolute error' else dict(vmin=0)
        im = ax.pcolormesh(t, x, field.T, shading='auto', rasterized=True, **kw)
        fig.colorbar(im, ax=ax); ax.set(title=label, xlabel='$t$', ylabel='$x$')
    for ax, target in zip(axes[1], [.25, .5, 1.]):
        i = int(np.argmin(abs(t - target)))
        ax.plot(x, ref[i], color='black', lw=1.2, label='Reference')
        ax.plot(x, pred[i], '--', color='#6f4798', lw=1, label='B67 corrected quadrature')
        ax.set(title=f'Profile at $t={t[i]:g}$', xlabel='$x$', ylabel='$u$'); ax.grid(alpha=.2)
    axes[1, 0].legend()
    fig.suptitle(f'Cosine KdV | relative L2 = {rel:.3e}; RMSE = {rmse:.3e}')
    export(fig, 'solution_and_error')

    steps = np.array([int(float(r['step'])) for r in history]); times = np.array([float(r['elapsed_seconds']) / 60 for r in history])
    errors = np.array([float(r['relative_l2']) for r in history])
    uncorrected = read_csv(ROOT / 'comparison_study/outputs/winner_b067_200k/reference_error_history.csv')
    previous_long = read_csv(ROOT / 'comparison_study/outputs/trial46_200k_150min/reference_error_history.csv')
    old_w = read_csv(ROOT / 'comparison_study/outputs/winner_046_30min/reference_error_history.csv')
    old_p = read_csv(ROOT / 'comparison_study/outputs/equal_steps_51573/piratenet_combined_error_history.csv')
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), layout='constrained')
    for ax, clock in zip(axes, [False, True]):
        ax.semilogy(times if clock else steps, errors, color='#6f4798', label='B67 corrected quadrature: 200k schedule')
        ax.semilogy([float(r['elapsed_seconds'])/60 if clock else int(float(r['step'])) for r in uncorrected],
                    [float(r['relative_l2']) for r in uncorrected], color='#b44141', lw=1, label='B67 original quadrature: 200k')
        ax.semilogy([float(r['elapsed_seconds'])/60 if clock else int(float(r['step'])) for r in previous_long],
                    [float(r['relative_l2']) for r in previous_long], color='#2675b9', lw=1, label='Original trial 46: 200k schedule')
        for rows, label, color in [(old_w, 'Trial 46: original 30-minute schedule', '#c07431'), (old_p, 'PirateNet port: stopped at 51,573 steps', '#39804a')]:
            xx = [float(r['training_seconds'])/60 if clock else int(float(r['step'])) for r in rows]
            ax.semilogy(xx, [float(r['relative_l2']) for r in rows], '-o', ms=2, lw=1, label=label, color=color)
        if not clock:
            ax.axvline(70000, color='gray', ls='--', lw=.8)
            ax.scatter([200000], [PAPER], color='black', marker='*', s=65, zorder=5, label='Published PirateNet: 200k endpoint')
        ax.set(xlabel='Run-loop minutes' if clock else 'Optimizer updates', ylabel='Relative $L^2$ error'); ax.grid(alpha=.2)
    axes[0].legend(fontsize=7)
    fig.suptitle('Observed errors; schedule, step budget and hardware costs differ')
    export(fig, 'error_comparison')

    training = [json.loads(line) for line in (OUT / 'training_history.jsonl').read_text().splitlines()]
    fig, axes = plt.subplots(2, 2, figsize=(11, 6), layout='constrained')
    for ax, key, title in zip(axes.ravel(), ['loss', 'lr', 'time_domain_upper', 'alpha'],
                            ['Total training loss (PDE + IC + invariants)', 'Learning rate', 'Upper training-time boundary', 'Learned IC envelope parameter (not error)']):
        rows = history if key == 'alpha' else training
        xx = [int(float(r['step'])) for r in rows]; yy = [float(r[key]) for r in rows]
        (ax.semilogy if key in ['loss', 'lr'] else ax.plot)(xx, yy, lw=1, color='#6f4798')
        ax.axvline(70000, color='gray', ls='--', lw=.8); ax.set(title=title, xlabel='Optimizer updates'); ax.grid(alpha=.2)
    export(fig, 'training_diagnostics')

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), layout='constrained')
    axes[0].semilogy(t, np.linalg.norm(error, axis=1)/np.linalg.norm(ref, axis=1), color='#6f4798')
    axes[0].set(title='Relative L2 at each physical time', xlabel='$t$', ylabel='Spatial relative $L^2$')
    axes[1].plot(x, error[-1], color='#6f4798'); axes[1].set(title='Signed final-time error', xlabel='$x$', ylabel=r'$u_\theta-u_{ref}$')
    for ax in axes: ax.grid(alpha=.2)
    export(fig, 'error_profiles')

    winner = json.loads((ROOT / 'comparison_study/outputs/winner_046_30min/evaluation.json').read_text())
    pirate = json.loads((ROOT / 'comparison_study/outputs/piratenet_matched_51573/test_01/metrics.json').read_text())
    prior_metrics = json.loads((ROOT / 'comparison_study/outputs/trial46_200k_150min/summary.json').read_text())
    uncorrected_metrics = json.loads((ROOT / 'comparison_study/outputs/winner_b067_200k/summary.json').read_text())
    rows = [dict(model='B67 original quadrature', steps=200000, relative_l2=uncorrected_metrics['final_metrics']['relative_l2'], rmse=uncorrected_metrics['final_metrics']['rmse'], training_seconds=uncorrected_metrics['loop_elapsed_seconds'], parameters=219650),dict(model='Original trial 46: 200k', steps=200000, relative_l2=prior_metrics['final_metrics']['relative_l2'],
                 rmse=prior_metrics['final_metrics']['rmse'], training_seconds=prior_metrics['loop_elapsed_seconds'], parameters=181442),dict(model='B67 corrected quadrature: 200k schedule', steps=state['step'], relative_l2=rel, rmse=rmse,
                 training_seconds=summary['loop_elapsed_seconds'], parameters=219650),
            dict(model='Trial 46: original 30min', steps=51573, relative_l2=winner['relative_l2'], rmse=winner['rmse'], training_seconds=winner['training_seconds'], parameters=181442),
            dict(model='PirateNet local port', steps=51573, relative_l2=pirate['relative_l2'], rmse=pirate['rmse'], training_seconds=7922.944509791, parameters=727171),
            dict(model='PirateNet published', steps=200000, relative_l2=PAPER, rmse='', training_seconds='', parameters='')]
    write_csv(OUT / 'comparison.csv', rows)
    table = '\n'.join(f"| {r['model']} | {r['steps']:,} | {r['relative_l2']:.5e} | {r['rmse']:.5e} |" if r['rmse'] != '' else f"| {r['model']} | {r['steps']:,} | {r['relative_l2']:.5e} | — |" for r in rows)
    (OUT / 'README.md').write_text(f'''# Frozen KdV-B67 corrected quadrature: completed 200,000-step cosine KdV run

Stopped at exactly **{state['step']:,} updates**, with no wall-clock cutoff. Run-loop time: **{summary['loop_elapsed_seconds']/60:.2f} minutes**. Final relative L2 **{rel:.5e}**, RMSE **{rmse:.5e}**. Paper threshold **{PAPER:.2e}** crossed at a recorded checkpoint: **{bool(below)}**. The first observed crossing, if any, is recorded in `first_below_paper.json` with its checkpoint and predictions. Final error is {rel/PAPER:.3f} times the published value; {winner['relative_l2']/rel:.3f} times lower than the original 30-minute winner result.

| Model / experiment | Updates | Relative L2 | RMSE |
|---|---:|---:|---:|
{table}

Same cosine IC, periodic KdV PDE and released 201 x 512 reference grid. Fresh model weights; step-based curriculum and optimizer mixing warmup through update 70,000, then cosine decay through 200,000. The selected sinusoidal network, SOAP-AdEMAMix optimizer and mass/energy penalty weights are retained. The only method change from the prior B67 long run is trapezoidal integration instead of the inclusive-grid mean rule. This is a test-informed corrected variant, not the original frozen candidate. This maps the selected winner's original time-based schedule to completed-step fractions. Test reference checks every 1,000 updates were diagnostic only; the scored checkpoint is final. Single seed, PyTorch/MPS. The local PirateNet ends at 51,573 updates, so this new endpoint is not an equal-step comparison against that local run. The paper value is published context, not a locally reproduced run or equal-FLOP benchmark.

Independent CPU audit reloads the final checkpoint, checks optimizer counters, re-computes reference metrics, checks exact reference coordinates/data and evaluates full-grid PDE/IC/periodicity. See `independent_verification.json`. CPU-reloaded predictions differ from saved MPS predictions by at most {max_difference:.3e}; official reported metrics use saved MPS predictions. Saved 5,000-step checkpoints were also scored independently in `checkpoint_errors_cpu.csv`.

![Solution and error](figures/solution_and_error.png)

![Observed error comparisons](figures/error_comparison.png)

Published PirateNet is shown only as a single marker at 200,000 updates, not a training trajectory. Its wall-clock time is unknown, so it is omitted from the time graph. Time curves have different diagnostics overhead; the new clock includes periodic evaluation/saves.

![Training diagnostics](figures/training_diagnostics.png)

![Error profiles](figures/error_profiles.png)

Rebuild audit and figures: `python comparison_study/runners/finish_winner_b67_trapezoid.py` from the repository root. No training is launched. PDF and PNG versions are in `figures/`; raw checkpoints, histories, predictions and final metadata are included.

Paper: [Wang et al., PirateNets (2024)](https://www.jmlr.org/papers/v25/24-0313.html).
''')
    console = Path(console) if console is not None else ROOT / 'winner_b067_trapezoid_console.log'
    if console.exists(): shutil.copy2(console, OUT / 'training_console.log')
    manifest = []
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.name != 'SHA256.json':
            manifest.append(dict(path=str(path.relative_to(OUT)), bytes=path.stat().st_size,
                                 sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    runner.dump(OUT / 'SHA256.json', manifest)
    print('Created four figures (PNG/PDF), scientific-notation comparison table and audit report.', flush=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--console', type=Path)
    args = parser.parse_args()
    main(args.output, args.console)
