# Equation contract

Model ID: `optical-dysthe-127-v1`. The migration target is the optical equation
implemented in the legacy repository's `src/dysthe_pinn/physics.py`:

```text
i E_t + (1 - i epsilon1 d_z)(E_xx + E_yy) - E_zz
      - i epsilon2 E_zzz + (1 + i epsilon1 d_z)(|E|^2 E) = 0.
```

Coordinates are propagation `t` and profile `(x,y,z)`; in the optical
interpretation, z is the relabeled normalized retarded time. The computational
domain is periodic. It does not certify whole-space behavior.

Do not silently substitute the different mixed-derivative sign in equation
(1.32), a water-wave equation, or a plasma equation. Resolve source conventions
before accepting a port. This document records a software target, not a new
derivation or theorem. Record a new model ID for any changed convention.

Arrays use complex128 `(time,x,y,z)`. ML adapters may use two real channels,
ordered `[real,imaginary]`, and must record their transforms and inverse.
Fit normalization using training data only. Preserve raw physical fields for
diagnostics. Keep grid, lengths, units/scaling, coefficients, observation times,
initial-condition group IDs, source commits, array hashes and refinement evidence.

Required reference checks: plane-wave/manufactured checks, independent nonlinear
RHS comparison, time refinement, grid refinement, domain sensitivity, projection
error and spectral-edge diagnostics. Conservation alone is insufficient.

`validate_case` checks metadata, not field-array accuracy. `validate_splits`
checks declared IDs; the generator must assign stable IDs to the same physical
initial condition across refinements, snapshots, seeds and augmentations.
