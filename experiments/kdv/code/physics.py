"""KdV residual and collocation stream from the 75-trial training implementation."""
import math
import torch
BATCH_SIZE=4096

def initial_condition(x,case):
    return (case['amplitude_1']*torch.cos(math.pi*case['frequency_1']*x)
           +case['amplitude_2']*torch.cos(math.pi*case['frequency_2']*x))

def physics_residual(model,tx):
    tx=tx.detach().clone().requires_grad_(True)
    u=model(tx)
    if u.shape!=(len(tx),1) or not bool(torch.isfinite(u).all()):
        raise ValueError('Model returned invalid output')
    du=torch.autograd.grad(u.sum(),tx,create_graph=True)[0]
    ut,ux=du[:,0:1],du[:,1:2]
    uxx=torch.autograd.grad(ux.sum(),tx,create_graph=True)[0][:,1:2]
    uxxx=torch.autograd.grad(uxx.sum(),tx,create_graph=True)[0][:,1:2]
    return ut+u*ux+0.022**2*uxxx

def physics_components(model,tx,case,x_ic):
    ph=physics_residual(model,tx).square().mean()
    ic_tx=torch.cat((torch.zeros_like(x_ic),x_ic),dim=1)
    ic=(model(ic_tx)-initial_condition(x_ic,case)).square().mean()
    return ph,ic

class TrainingBatchStream:
    def __init__(self,device,seed,batch_size=BATCH_SIZE):
        self.device=device;self.batch_size=batch_size;self.count=0
        self.generator=torch.Generator(device=device.type if device.type in ('cpu','cuda') else 'cpu').manual_seed(seed)
    def next(self):
        self.count+=1
        pts=torch.rand((self.batch_size,2),generator=self.generator,device=self.device if self.device.type!='mps' else 'cpu')
        pts[:,1]=pts[:,1]*2-1
        return pts.to(self.device)
