# Sitnikov restricted three-body problem

Two equal-mass primaries follow a planar Kepler orbit; a massless third body moves along the perpendicular axis. The PINN predicts vertical position z(t) and velocity v(t):

\[
z'=v,\qquad v'=-\frac{z}{(z^2+\rho(t,e)^2)^{3/2}},\qquad
\rho=\frac{1-e\cos E}{2},\quad E-e\sin E=t\pmod{2\pi}.
\]

Fifty autonomous trials explored neural representations and training methods across ten development initial conditions. Training uses 500 sampled time coordinates over [0,6π]; 2,000 separate physics-validation coordinates guide method selection. Numerical trajectories are reserved for the later evaluation on ten held-out IVPs.

Selected **Trial 049** uses eight learnable Fourier frequencies initialised at k/3, a width-192 modified gated PINN and Adam β=(0.99,0.99), with scheduled initial-condition weighting. Each case receives fresh weights.

| Mean held-out in-interval RMSE | Original baseline | Trial 049 | Reduction |
|---|---:|---:|---:|
| Position | 1.690474 | 0.957983 | 43.33% |
| Velocity | 0.731735 | 0.450944 | 38.37% |

The original baseline trained for about 4.74 seconds per case, versus 87.01 seconds for Trial 049, within the same 90-second cap. These percentages describe the original baseline comparison.

![Position trajectories](../../figures/sitnikov_position.png)

*Predicted positions and DOP853 reference trajectories for the ten held-out IVPs.*

![Velocity trajectories](../../figures/sitnikov_velocity.png)

*Velocity on the same cases and interval; variables are nondimensional.*

[Experimental report](report.md) · [50 trial decisions](decisions/README.md) · [Selected model and training code](code/selected_candidate.py) · [Results](results/)
