#!/usr/bin/env node
/**
 * Parity runner — TypeScript side.
 *
 *   node parity/run-ts.mjs emit         run every shared case, record observations
 *   node parity/run-ts.mjs cross-open   open the Python output, compare both bindings
 *
 * This harness is test-only: it imports the *built* frozen binding from `dist/`, never
 * `src/`, and it never turns either binding's current output into an expectation.
 * Observations are normalized exactly as `parity/harness.py` normalizes them: the
 * differences the contract allows (binding-dependent hashes, `1` vs `1.0`, an explicit
 * null vs an omitted optional *model field*, key insertion order) are erased, nothing
 * else. A null value inside an opaque producer-authored map is not such a difference;
 * the `read_document` operation marks those nulls so they survive normalization.
 */

import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";
import Ajv from "ajv";
import { parse } from "yaml";

import {
  abandonExperiment,
  addAssessment,
  addClaim,
  addDataset,
  addEnvironment,
  addExhibit,
  addExperiment,
  addResult,
  addTrace,
  attachPaper,
  attachResearchAgent,
  computeEvidenceInventory,
  configureJournal,
  createArtifact,
  defaultExhibitValidationMode,
  defaultValidationMode,
  failExperiment,
  getAssessment,
  getClaim,
  getDataset,
  getExhibit,
  getExperiment,
  getResult,
  getTrace,
  listAbandonedExperiments,
  listAssessments,
  listClaims,
  listDatasets,
  listExhibits,
  listExperiments,
  listJournal,
  listResults,
  listTraces,
  openSubmission,
  pinnedDigest,
  purgeExperiment,
  removeAssessment,
  removeClaim,
  removeDataset,
  removeExhibit,
  removeExperiment,
  removeResult,
  removeTrace,
  setReflection,
  supersedeExperiment,
  validateStructure,
  writeSubmission,
} from "../dist/index.js";

const PARITY_ROOT = dirname(fileURLToPath(import.meta.url));
const CASES_DIR = join(PARITY_ROOT, "cases");
const SCRATCH_DIR = join(PARITY_ROOT, ".scratch");
const TS_ROOT = join(SCRATCH_DIR, "ts");
const PY_ROOT = join(SCRATCH_DIR, "py");
const TS_OBSERVATIONS = join(SCRATCH_DIR, "observations", "ts");
const PY_OBSERVATIONS = join(SCRATCH_DIR, "observations", "py");
const HASH_PLACEHOLDER = "<sha256>";
const NULL_PLACEHOLDER = "<null>";
const INDEX_DOCUMENTS = [
  "manifest.yml",
  "claims.yml",
  "results.yml",
  "datasets.yml",
  "exhibits.yml",
  "traces.yml",
  "assessments.yml",
  "journal.yml",
];

function fail(message) {
  console.error(`parity(typescript): ${message}`);
  process.exit(1);
}

// --- normalization ----------------------------------------------------------

function normalize(value) {
  if (value === null || value === undefined) return undefined;
  if (typeof value === "number") return Number.isInteger(value) ? value : value;
  if (Array.isArray(value)) return value.map((item) => normalize(item));
  if (typeof value === "object") {
    const result = {};
    for (const [key, item] of Object.entries(value)) {
      if (item === null || item === undefined) continue;
      const normalized = normalize(item);
      if (normalized === undefined) continue;
      const empty =
        (Array.isArray(normalized) && normalized.length === 0) ||
        (typeof normalized === "object" &&
          !Array.isArray(normalized) &&
          Object.keys(normalized).length === 0);
      if (empty) continue;
      result[key] = normalized;
    }
    return result;
  }
  return value;
}

function normalizeModel(artifact) {
  return normalize({ ...artifact, journalConfig: undefined });
}

/**
 * Replace every explicit null with `NULL_PLACEHOLDER`.
 *
 * Normalization treats a null as an omitted optional field, which is the reviewed
 * divergence for *model fields* only. A null value inside an opaque producer-authored map
 * — `producer`, `run.env`, `counters`, `locators`, a validator's `input`/`params` — is
 * data both bindings must keep, so `read_document` marks it and the marker survives
 * normalization.
 */
function markNulls(value) {
  if (value === null || value === undefined) return NULL_PLACEHOLDER;
  if (Array.isArray(value)) return value.map((item) => markNulls(item));
  if (typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, markNulls(item)]),
    );
  }
  return value;
}

/** Walk a document by a key/index path, e.g. ["experiments", 0, "run", "env"]. */
function selectPath(value, path) {
  let current = value;
  for (const key of path) current = current[key];
  return current;
}

/** Stable, key-order-insensitive rendering used for comparison and diagnostics. */
function canonical(value) {
  return JSON.stringify(sortKeys(value === undefined ? null : value), null, 2);
}

function sortKeys(value) {
  if (Array.isArray(value)) return value.map(sortKeys);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, sortKeys(value[key])]),
    );
  }
  return value;
}

function expectEqual(label, actual, expected) {
  if (canonical(actual) !== canonical(expected)) {
    fail(
      `${label}\n--- actual ---\n${canonical(actual)}\n--- expected ---\n${canonical(expected)}`,
    );
  }
}

// --- filesystem observation --------------------------------------------------

function walkFiles(root, dir = root, acc = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const abs = join(dir, entry.name);
    if (entry.isDirectory()) walkFiles(root, abs, acc);
    else acc.push(relative(root, abs).split(sep).join("/"));
  }
  return acc;
}

function normalizeSums(text) {
  return text
    .split("\n")
    .filter((line) => line.trim().length > 0)
    .map((line) => `${HASH_PLACEHOLDER}  ${line.slice(line.indexOf("  ") + 2)}`)
    .sort();
}

function readState(outDir) {
  const statePath = join(outDir, ".sdk", "state.json");
  if (!existsSync(statePath)) return {};
  const state = JSON.parse(readFileSync(statePath, "utf-8"));
  return {
    generated_files: [...(state.generated_files ?? [])].sort(),
    authored_files: Object.keys(state.authored_files ?? {}).sort(),
  };
}

function observeOutput(outDir) {
  const files = walkFiles(outDir).sort();
  const documents = {};
  for (const name of INDEX_DOCUMENTS) {
    if (existsSync(join(outDir, name))) {
      documents[name] = normalize(parse(readFileSync(join(outDir, name), "utf-8")) ?? {});
    }
  }
  const markers = {};
  for (const path of files) {
    if (path.endsWith("DISPOSITION.md")) {
      markers[path] = readFileSync(join(outDir, path), "utf-8");
    }
  }
  const observation = {
    files,
    state: readState(outDir),
    sums: existsSync(join(outDir, "SHA256SUMS"))
      ? normalizeSums(readFileSync(join(outDir, "SHA256SUMS"), "utf-8"))
      : [],
    documents,
    disposition_markers: markers,
  };
  if (existsSync(join(outDir, "reflection.md"))) {
    observation.reflection = readFileSync(join(outDir, "reflection.md"), "utf-8");
  }
  return observation;
}

function observeReport(report) {
  return {
    ok: report.ok,
    incomplete: report.incomplete,
    warning_paths: report.warnings.map((issue) => issue.path),
    files_written: [...report.filesWritten].sort(),
    missing_blobs: [...report.missingBlobs].sort(),
  };
}

/** Validate raw case data against the canonical draft-07 schema (§6.1). */
function observeSchema(artifactData) {
  const schema = JSON.parse(
    readFileSync(join(PARITY_ROOT, "..", "schema", "evaluable-artifact-v2.schema.json"), "utf-8"),
  );
  const ajv = new Ajv({ strict: false, allErrors: true });
  const validate = ajv.compile(schema);
  const valid = validate(artifactData);
  const paths = [...new Set((validate.errors ?? []).map((error) => error.instancePath))].sort();
  return { valid: Boolean(valid), paths };
}

function observeValidation(report) {
  return {
    ok: report.ok,
    error_paths: report.errors.map((issue) => issue.path),
    warning_paths: report.warnings.map((issue) => issue.path),
  };
}

// --- operation dispatch -------------------------------------------------------

function context(step) {
  return step.context ? { actor: step.context.actor, rationale: step.context.rationale } : undefined;
}

function makeOperations(session) {
  const current = () => {
    if (!session.artifact) throw new Error("operation case: create_artifact must run first");
    return session.artifact;
  };
  const resolve = (relativePath) => join(session.outRoot, relativePath);
  return {
    default_validation_mode: (args) => defaultValidationMode(args.kind),
    default_exhibit_validation_mode: (args) => defaultExhibitValidationMode(args.type),
    pinned_digest: (args) => pinnedDigest(args.reference) ?? null,
    create_artifact: (args) => {
      session.artifact = createArtifact({
        id: args.id,
        title: args.title,
        producer: args.producer,
      });
      return undefined;
    },
    configure_journal: (args) => {
      if (args.now) {
        session.nowValues = [...args.now];
        session.nowIndex = 0;
      }
      configureJournal(current(), {
        policy: args.policy,
        actor: args.actor,
        onMissingRationale:
          args.prompt_rationale !== undefined ? () => args.prompt_rationale : undefined,
        now: () => session.nowValues[Math.min(session.nowIndex++, session.nowValues.length - 1)],
      });
      return undefined;
    },
    prepare_file: (args) => {
      const target = resolve(args.path);
      mkdirSync(dirname(target), { recursive: true });
      writeFileSync(target, args.content ?? "", "utf-8");
      return undefined;
    },
    read_file: (args) => readFileSync(resolve(args.path), "utf-8"),
    read_document: (args) =>
      markNulls(
        selectPath(parse(readFileSync(resolve(args.path), "utf-8")) ?? {}, args.select ?? []),
      ),
    write_submission: (args) =>
      observeReport(
        writeSubmission(current(), resolve(args.out ?? "out"), {
          stageFrom: args.stage_from ? join(PARITY_ROOT, args.stage_from) : undefined,
          quiet: args.quiet ?? false,
        }),
      ),
    open_submission: (args) => {
      const artifact = openSubmission(resolve(args.out ?? "out"));
      // Continue the script from the reopened artifact, so a later write exercises the
      // reopen → write round trip.
      if (args.into_session) session.artifact = artifact;
      return normalizeModel(artifact);
    },
    validate_structure: () => observeValidation(validateStructure(current())),
    compute_evidence_inventory: () => normalize(computeEvidenceInventory(current())),
    add_environment: (args, step) => normalize(addEnvironment(current(), args, context(step))),
    add_dataset: (args, step) => normalize(addDataset(current(), args, context(step))),
    add_experiment: (args, step) => normalize(addExperiment(current(), args, context(step))),
    add_trace: (args, step) => normalize(addTrace(current(), args, context(step))),
    add_result: (args, step) => normalize(addResult(current(), args, context(step))),
    add_exhibit: (args, step) => normalize(addExhibit(current(), args, context(step))),
    add_claim: (args, step) => normalize(addClaim(current(), args, context(step))),
    add_assessment: (args, step) => normalize(addAssessment(current(), args, context(step))),
    attach_paper: (args, step) => normalize(attachPaper(current(), args, context(step))),
    attach_research_agent: (args, step) =>
      normalize(attachResearchAgent(current(), args, context(step))),
    set_reflection: (args, step) => setReflection(current(), args.markdown, context(step)),
    abandon_experiment: (args, step) =>
      normalize(abandonExperiment(current(), args.slug, context(step))),
    fail_experiment: (args, step) =>
      normalize(failExperiment(current(), args.slug, args.failure, context(step))),
    supersede_experiment: (args, step) =>
      normalize(supersedeExperiment(current(), args.slug, args.superseded_by, context(step))),
    purge_experiment: (args, step) => purgeExperiment(current(), args.slug, context(step)),
    remove_experiment: (args, step) => removeExperiment(current(), args.slug, context(step)),
    remove_dataset: (args, step) => removeDataset(current(), args.id, context(step)),
    remove_trace: (args, step) => removeTrace(current(), args.id, context(step)),
    remove_result: (args, step) => removeResult(current(), args.id, context(step)),
    remove_exhibit: (args, step) => removeExhibit(current(), args.id, context(step)),
    remove_claim: (args, step) => removeClaim(current(), args.id, context(step)),
    remove_assessment: (args, step) => removeAssessment(current(), args.id, context(step)),
    get_dataset: (args) => normalize(getDataset(current(), args.id)),
    get_experiment: (args) => normalize(getExperiment(current(), args.slug)),
    get_trace: (args) => normalize(getTrace(current(), args.id)),
    get_result: (args) => normalize(getResult(current(), args.id)),
    get_exhibit: (args) => normalize(getExhibit(current(), args.id)),
    get_claim: (args) => normalize(getClaim(current(), args.id)),
    get_assessment: (args) => normalize(getAssessment(current(), args.id)),
    list_datasets: () => normalize(listDatasets(current())),
    list_experiments: () => normalize(listExperiments(current())),
    list_abandoned_experiments: () => normalize(listAbandonedExperiments(current())),
    list_traces: () => normalize(listTraces(current())),
    list_results: () => normalize(listResults(current())),
    list_exhibits: () => normalize(listExhibits(current())),
    list_claims: () => normalize(listClaims(current())),
    list_assessments: () => normalize(listAssessments(current())),
    list_journal: () => normalize(listJournal(current())),
  };
}

// --- case execution -----------------------------------------------------------

function loadCases() {
  return readdirSync(CASES_DIR)
    .filter((name) => name.endsWith(".json"))
    .sort()
    .map((name) => JSON.parse(readFileSync(join(CASES_DIR, name), "utf-8")));
}

function caseOutDir(root, testCase) {
  return join(root, testCase.name);
}

function runArtifactCase(testCase, outRoot) {
  const artifact = structuredClone(testCase.artifact);
  const report = validateStructure(artifact);
  const observation = {
    name: testCase.name,
    kind: "artifact",
    validation: observeValidation(report),
    schema: observeSchema(testCase.artifact),
    model: normalizeModel(artifact),
  };
  if (!report.ok) return observation;
  const write = testCase.write ?? {};
  const outDir = join(outRoot, "out");
  const result = writeSubmission(artifact, outDir, {
    stageFrom: write.stage_from ? join(PARITY_ROOT, write.stage_from) : undefined,
    quiet: write.quiet ?? false,
  });
  observation.write = observeReport(result);
  observation.output = observeOutput(outDir);
  observation.reopened = normalizeModel(openSubmission(outDir));
  // A write → open → write round trip is idempotent within a binding (§8.7).
  const reopenedDir = join(outRoot, "reopened");
  mkdirSync(reopenedDir, { recursive: true });
  for (const name of observation.output.files) {
    mkdirSync(dirname(join(reopenedDir, name)), { recursive: true });
    copyFileSync(join(outDir, name), join(reopenedDir, name));
  }
  writeSubmission(openSubmission(reopenedDir), reopenedDir);
  observation.idempotent =
    canonical(observeOutput(reopenedDir).documents) === canonical(observation.output.documents);
  return observation;
}

function runOperationCase(testCase, outRoot) {
  const session = {
    artifact: undefined,
    outRoot,
    nowValues: ["1970-01-01T00:00:00.000Z"],
    nowIndex: 0,
  };
  const operations = makeOperations(session);
  const steps = [];
  testCase.operations.forEach((step, index) => {
    const handler = operations[step.operation];
    if (!handler) fail(`${testCase.name}: unknown operation '${step.operation}'`);
    const record = { index, operation: step.operation };
    let raised = false;
    let returned;
    try {
      returned = handler(step.arguments ?? {}, step);
    } catch (error) {
      raised = true;
      if (!step.expects_error) {
        fail(`${testCase.name} step ${index} (${step.operation}) raised unexpectedly: ${error}`);
      }
    }
    if (raised) record.raised = true;
    else {
      if (step.expects_error) {
        fail(`${testCase.name} step ${index} (${step.operation}) was expected to raise`);
      }
      const normalized = normalize(returned);
      record.returned = normalized === undefined ? null : normalized;
    }
    steps.push(record);
  });
  const observation = {
    name: testCase.name,
    kind: "operation",
    steps,
    model: normalizeModel(session.artifact),
    validation: observeValidation(validateStructure(session.artifact)),
  };
  const outDir = join(outRoot, "out");
  if (existsSync(join(outDir, "manifest.yml"))) {
    observation.output = observeOutput(outDir);
    observation.reopened = normalizeModel(openSubmission(outDir));
  }
  return observation;
}

function runCase(testCase, root) {
  const outRoot = caseOutDir(root, testCase);
  rmSync(outRoot, { recursive: true, force: true });
  mkdirSync(outRoot, { recursive: true });
  return testCase.kind === "artifact"
    ? runArtifactCase(testCase, outRoot)
    : runOperationCase(testCase, outRoot);
}

function checkExpectations(testCase, observation) {
  const expected = testCase.expected;
  const name = testCase.name;
  expectEqual(`${name}: validation.ok`, observation.validation.ok, expected.ok);
  expectEqual(`${name}: error paths`, observation.validation.error_paths, expected.error_paths);
  expectEqual(
    `${name}: warning paths`,
    observation.validation.warning_paths,
    expected.warning_paths,
  );
  if (expected.schema_valid !== undefined) {
    expectEqual(`${name}: schema validity`, observation.schema.valid, expected.schema_valid);
  }
  for (const path of expected.schema_error_paths ?? []) {
    if (!observation.schema.paths.includes(path)) {
      fail(`${name}: expected a schema error at '${path}', got ${observation.schema.paths}`);
    }
  }
  if (expected.model !== undefined) expectEqual(`${name}: model`, observation.model, expected.model);
  if (expected.report !== undefined) {
    expectEqual(`${name}: write report`, observation.write, expected.report);
  }
  if (expected.output !== undefined) {
    for (const [key, value] of Object.entries(expected.output)) {
      expectEqual(`${name}: output.${key}`, observation.output[key], value);
    }
  }
  if (expected.state !== undefined) {
    expectEqual(`${name}: state`, observation.output.state, expected.state);
  }
  if (expected.reopened !== undefined) {
    expectEqual(`${name}: reopened model`, observation.reopened, expected.reopened);
  }
  if (expected.steps !== undefined) expectEqual(`${name}: steps`, observation.steps, expected.steps);
  for (const [index, value] of Object.entries(expected.step_returns ?? {})) {
    const step = observation.steps[Number(index)];
    expectEqual(`${name}: step ${index} (${step.operation}) return`, step.returned ?? null, value);
  }
  for (const index of expected.raising_steps ?? []) {
    const step = observation.steps[Number(index)];
    if (!step.raised) fail(`${name}: step ${index} (${step.operation}) was expected to raise`);
  }
  if (observation.idempotent === false) {
    fail(`${name}: write → open → write was not idempotent`);
  }
}

function emit() {
  rmSync(TS_ROOT, { recursive: true, force: true });
  rmSync(TS_OBSERVATIONS, { recursive: true, force: true });
  mkdirSync(TS_OBSERVATIONS, { recursive: true });
  const cases = loadCases();
  for (const testCase of cases) {
    const observation = runCase(testCase, TS_ROOT);
    checkExpectations(testCase, observation);
    writeFileSync(
      join(TS_OBSERVATIONS, `${testCase.name}.json`),
      `${canonical(observation)}\n`,
      "utf-8",
    );
  }
  console.log(`parity(typescript): ${cases.length} cases emitted`);
}

function crossOpen() {
  const cases = loadCases();
  let compared = 0;
  for (const testCase of cases) {
    const name = testCase.name;
    const minePath = join(TS_OBSERVATIONS, `${name}.json`);
    const theirsPath = join(PY_OBSERVATIONS, `${name}.json`);
    if (!existsSync(minePath)) fail(`${name}: missing TypeScript observation — run \`emit\` first`);
    if (!existsSync(theirsPath)) fail(`${name}: missing Python observation — run the Python runner`);
    const mine = JSON.parse(readFileSync(minePath, "utf-8"));
    const theirs = JSON.parse(readFileSync(theirsPath, "utf-8"));
    for (const key of ["validation", "write", "model", "reopened", "steps", "output"]) {
      if (key in mine || key in theirs) {
        expectEqual(`${name}: ${key} differs between bindings`, mine[key] ?? null, theirs[key] ?? null);
      }
    }
    if ("schema" in mine || "schema" in theirs) {
      // Both bindings must accept or reject the same artifact; the two schema libraries
      // report sub-schema failures at different granularity, so only the verdict is a
      // cross-binding contract (PYTHON_BINDING.md §8.1).
      expectEqual(
        `${name}: schema verdict differs between bindings`,
        mine.schema?.valid ?? null,
        theirs.schema?.valid ?? null,
      );
    }
    if (mine.reopened === undefined) {
      compared += 1;
      continue;
    }
    const pyOut = join(caseOutDir(PY_ROOT, testCase), "out");
    if (!existsSync(join(pyOut, "manifest.yml"))) fail(`${name}: Python output is missing at ${pyOut}`);
    const cross = normalizeModel(openSubmission(pyOut));
    expectEqual(`${name}: TypeScript reopening Python output`, cross, mine.reopened);
    compared += 1;
  }
  console.log(`parity(typescript): ${compared} cases cross-opened and compared`);
}

const phase = process.argv[2] ?? "emit";
if (phase === "emit") emit();
else if (phase === "cross-open") crossOpen();
else fail(`unknown phase '${phase}' (expected 'emit' or 'cross-open')`);
