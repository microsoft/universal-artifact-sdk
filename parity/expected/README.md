# Reviewed parity expectations

Each case under [`../cases`](../cases) carries its own reviewed `expected` block, so a
case and the contract it asserts stay in one reviewable file. The block is described by
[`../case.schema.json`](../case.schema.json) and covers validation severity and issue
paths, the canonical-schema verdict, the write report, the on-disk ledger, the emitted
documents, and the in-memory and reopened models.

## How a case is checked

1. Each runner (`../run-ts.mjs`, `../run_py.py`) executes every case against its own
   binding and reduces the run to a **normalized observation**.
2. Normalization erases only the differences the contract allows: binding-dependent
   hashes, numerically equal integral values such as `1` and `1.0`, an explicit `null`
   versus an omitted optional **model field**, an empty collection versus an omitted one,
   and key insertion order. Nothing else is erased. A null *value inside an opaque
   producer-authored map* is data, not an absent field: the `read_document` operation
   marks such nulls as `<null>` so they survive normalization and are compared across
   bindings.
3. Each runner asserts the reviewed `expected` block.
4. `cross-open` then asserts that both bindings' observations are equal, that Python
   reopens the TypeScript output into the same normalized model, and that TypeScript
   reopens the Python output into the same normalized model.

## Rules

- Expectations are human-reviewed contract data. A runner may never turn a binding's
  current output into an expectation; there is no implicit `--update` path.
- When a reviewed expectation and a binding disagree, the binding is wrong until a
  maintainer decides otherwise in review.
- Case names are stable: they name the scratch directories under `../.scratch` and the
  observation files under `../.scratch/observations`.
