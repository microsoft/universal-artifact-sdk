// Universal Artifact SDK — end-to-end quickstart.
//
// Run it from the SDK package (after `npm install && npm run build`):
//
//     node examples/quickstart.mjs
//
// It builds a minimal but complete artifact — one experiment, one result, one
// claim backed by a deterministic validator, and a paper — then writes a
// conforming `evaluable-artifact/v2` submission a downstream evaluator can evaluate.
//
// The imports below use the package's own name, so this file is exactly what a
// producer copies into their own project (Node resolves it via the package
// `exports`). Only the two Node stdlib imports are here to fabricate a tiny
// evidence file + placeholder paper so the example is self-contained; a real
// producer already has these on disk and just points `stageFrom` at their root.

import { mkdtempSync, mkdirSync, writeFileSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import {
  createArtifact,
  configureJournal,
  addEnvironment,
  addExperiment,
  addResult,
  addClaim,
  attachPaper,
  writeSubmission,
} from "@microsoft/universal-artifact-sdk";

// --- 0. a producer already has these files on disk; we fabricate them here ---
const source = mkdtempSync(join(tmpdir(), "uas-quickstart-src-"));
mkdirSync(join(source, "experiments", "accuracy"), { recursive: true });
writeFileSync(
  join(source, "experiments", "accuracy", "metrics.csv"),
  "metric,value\naccuracy,0.91\n",
  "utf-8",
);
writeFileSync(join(source, "paper.pdf"), "%PDF-1.4 placeholder\n", "utf-8");

// --- 1. declare the structured facts the producer already knows ---------------
const a = createArtifact({ id: "quickstart-1", title: "A minimal reproducible artifact" });

// Every mutation is journaled with a rationale (the "why", which a VCS diff can't
// recover). Set the default actor once; each call below passes a short rationale.
configureJournal(a, { actor: "quickstart", policy: "warn" });

// The environment is recorded by reference; pin the immutable digest so the exact
// image is recoverable (a bare tag is mutable). The SDK also lifts a digest that
// is already embedded in the reference (`repo@sha256:...`).
addEnvironment(
  a,
  {
    name: "primary",
    image: { reference: "ghcr.io/example/artifact:1.0", digest: "sha256:" + "0".repeat(64) },
  },
  { rationale: "pin the run image so the environment is reproducible" },
);

addExperiment(
  a,
  {
    slug: "accuracy",
    directory: "experiments/accuracy",
    run: { command: "python run.py --seed 0", entrypoint: "run.py", seed: 0 },
    runs_in: "primary",
  },
  { rationale: "the benchmark run backing the accuracy claim" },
);

// A Result points at the evidence file and names the cell that backs the number.
addResult(
  a,
  {
    id: "R1",
    produced_by: "accuracy",
    validates: ["C1"],
    evidence: "experiments/accuracy/metrics.csv",
    kind: "metrics",
    locators: { accuracy: { column: "value", row: "accuracy" } },
  },
  { rationale: "records the measured accuracy" },
);

// A Claim binds a paper statement to a deterministic check over that Result —
// here "the reported 0.91 is what the artifact produced (within tolerance)".
addClaim(
  a,
  {
    id: "C1",
    statement: "The method reaches 0.91 accuracy on the benchmark.",
    paper_ref: { section: "4.1", figure: "2" },
    validator: {
      kind: "builtin",
      name: "numeric_close",
      input: { result: "R1", locator: { column: "value", row: "accuracy" } },
      params: { expected: 0.91, rel_tol: 0.05 },
    },
  },
  { rationale: "the headline result claim, checked against the shipped metrics" },
);

attachPaper(a, { pdf: "paper.pdf" }, { rationale: "the compiled paper" });

// --- 2. write a conforming submission ----------------------------------------
// `stageFrom` copies the referenced blobs (evidence, paper) in from the source
// root. Generated index files (manifest/claims/results/...) are written by the SDK.
const out = mkdtempSync(join(tmpdir(), "uas-quickstart-out-"));
const report = writeSubmission(a, out, { stageFrom: source });

// --- 3. report ----------------------------------------------------------------
console.log(`Wrote ${report.filesWritten.length} files to:\n  ${out}\n`);
console.log("Files:");
for (const f of report.filesWritten) console.log("  " + f);

if (report.incomplete) {
  console.warn("\nIncomplete (warnings):");
  for (const w of report.warnings) console.warn("  - " + w.message);
} else {
  console.log("\nSubmission is complete. manifest.yml:\n");
  console.log(readFileSync(join(out, "manifest.yml"), "utf-8"));
}
