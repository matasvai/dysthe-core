# First migration

Source: matasvai/dysthe-pinn at `bca8aa3833d79e5030ed53efab3bd94c9480aa54` (existing collaborator access required).

1. On `codex/reference-migration`, port `src/dysthe_pinn/reference.py`, the
   equation specification, and applicable independent physics tests.
2. Preserve the legacy solver in place until identical-input comparisons pass.
   Record upstream revision and file hashes in the port PR.
3. Put initial-condition generation under `initial_conditions/`, independently
   test width/box behavior, and add families on `codex/initial-condition-family`.
4. Port diagnostic norms and refinement logic only after checking their optical
   field meanings. Extract general pieces from `field_fno/metrics.py` as needed.
5. Publish a pinned core revision before updating learning and experiment repos.

No legacy source or historical run files have been copied by this scaffold.
