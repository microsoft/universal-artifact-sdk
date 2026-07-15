import { mkdtempSync, readFileSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { afterAll, describe, expect, it } from "vitest";
import Ajv from "ajv";
import { parse } from "yaml";

import {
  Artifact,
  addClaim,
  addDataset,
  addEnvironment,
  addExperiment,
  addResult,
  addTrace,
  attachPaper,
  createArtifact,
  openSubmission,
  writeSubmission,
} from "../src/index.js";

const here = dirname(fileURLToPath(import.meta.url));
const FIXTURE_SRC = join(here, "fixtures", "source");
const SCHEMA = join(here, "..", "schema", "evaluable-artifact-v2.schema.json");

const tmpDirs: string[] = [];
function scratch(): string {
  const d = mkdtempSync(join(tmpdir(), "uas-test-"));
  tmpDirs.push(d);
  return d;
}
afterAll(() => {
  for (const d of tmpDirs) rmSync(d, { recursive: true, force: true });
});

/** Build the Appendix A worked example (spec §Appendix A). */
function buildWorkedExample(): Artifact {
  const a = createArtifact({ id: "expt-42", title: "Feedback-driven contraction" });
  addEnvironment(a, {
    name: "primary",
    image: { reference: "reg/artifact:1.2", digest: "sha256:abc" },
  });
  addDataset(a, {
    id: "sample_corpus",
    location: {
      kind: "external",
      uri: "https://example.org/corpus-v3.tar.gz",
      bytes: 294721271,
      sha256: "def",
      access: "public",
    },
    prepare: "tar -xzf corpus-v3.tar.gz -C ./data",
  });
  addExperiment(a, {
    slug: "posterior_contraction",
    directory: "experiments/posterior_contraction",
    run: { command: "python run.py --seed 0", entrypoint: "run.py", seed: 0 },
    uses_data: [{ dataset: "sample_corpus", at: "data/corpus.parquet" }],
    runs_in: "primary",
  });
  addResult(a, {
    id: "R1",
    produced_by: "posterior_contraction",
    validates: ["C1"],
    evidence: "experiments/posterior_contraction/contraction.csv",
    kind: "metrics",
    locators: {
      kl_final: { column: "kl_divergence", row: "final" },
      kl_initial: { column: "kl_divergence", row: "0" },
    },
  });
  addClaim(a, {
    id: "C1",
    statement: "Posterior contraction improves with more feedback rounds.",
    paper_ref: { section: "5.2", figure: "3" },
    validator: {
      kind: "builtin",
      name: "monotonic",
      input: { result: "R1", series: ["kl_initial", "kl_final"] },
      params: { direction: "decreasing" },
    },
  });

  // qualitative claim: transcript evidence, attest-gates-inspect, a trace
  addDataset(a, {
    id: "interviews",
    location: { kind: "in_artifact", path: "data/interviews/" },
    study: {
      ethics_approval: "IRB-2025-0142",
      consent_basis: "informed, opt-in",
      deidentification: "names redacted",
      sampling: "convenience; n=18",
    },
  });
  addTrace(a, {
    id: "T1",
    kind: "agent_session",
    path: "traces/run_0007.jsonl",
    covers: ["posterior_contraction"],
    terminal_state: "completed_with_outputs",
  });
  addResult(a, {
    id: "R2",
    validates: ["C7"],
    evidence: "data/interviews/",
    kind: "transcript",
    validation_mode: "inspect",
    support: {
      excerpts: [{ file: "data/interviews/P07.txt", lines: "40-55" }],
      inter_rater_reliability: { metric: "cohen_kappa", value: 0.81 },
    },
  });
  addClaim(a, {
    id: "C7",
    statement: "Participants distrusted the tool's suggestions.",
    paper_ref: { section: "6.1" },
    validators: [
      { id: "v_attest", kind: "attest", checks: "provenance", inputs: ["R2"] },
      {
        id: "v_inspect",
        kind: "llm_judge",
        gated_by: "v_attest",
        criteria: "The cited excerpts express distrust of the tool's suggestions.",
        inputs: ["R2"],
      },
    ],
  });
  attachPaper(a, {
    pdf: "paper.pdf",
    source: "paper/",
    references_export: "paper_references.yml",
  });
  return a;
}

describe("writeSubmission — worked example (Appendix A)", () => {
  it("emits the evaluable-artifact/v2 on-disk layout", () => {
    const out = scratch();
    const report = writeSubmission(buildWorkedExample(), out, { stageFrom: FIXTURE_SRC });

    expect(report.ok).toBe(true);
    expect(report.missingBlobs).toEqual([]);

    for (const f of [
      "manifest.yml",
      "claims.yml",
      "results.yml",
      "datasets.yml",
      "traces.yml",
      "SHA256SUMS",
      ".sdk/state.json",
    ]) {
      expect(existsSync(join(out, f)), `${f} should exist`).toBe(true);
    }
    // no assessments were declared → the index file is omitted (spec §5)
    expect(existsSync(join(out, "assessments.yml"))).toBe(false);

    // staged blobs are present
    expect(existsSync(join(out, "experiments/posterior_contraction/contraction.csv"))).toBe(true);
    expect(existsSync(join(out, "data/interviews/P07.txt"))).toBe(true);
    expect(existsSync(join(out, "traces/run_0007.jsonl"))).toBe(true);
    expect(existsSync(join(out, "paper.pdf"))).toBe(true);
  });

  it("stamps format_version and computes the evidence inventory", () => {
    const out = scratch();
    writeSubmission(buildWorkedExample(), out, { stageFrom: FIXTURE_SRC });
    const manifest = parse(readFileSync(join(out, "manifest.yml"), "utf-8"));

    expect(manifest.format_version).toBe("evaluable-artifact/v2");
    expect(manifest.sdk_version).toBe("artifact-sdk/v1");
    expect(manifest._generated).toContain("artifact-sdk/v1");

    const inv = manifest.evidence_inventory;
    expect(inv.has_runnable_experiments).toBe(true);
    expect(inv.has_traces).toBe(true);
    expect(inv.trace_count).toBe(1);
    expect(inv.has_released_data).toBe(true);
    expect(inv.has_citations_export).toBe(true);
    expect(inv.evidence_kinds).toContain("metrics");
    expect(inv.evidence_kinds).toContain("transcript");
    expect(inv.validation_modes).toContain("inspect");
  });

  it("serializes claims with the validator list and gated_by edge", () => {
    const out = scratch();
    writeSubmission(buildWorkedExample(), out, { stageFrom: FIXTURE_SRC });
    const claims = parse(readFileSync(join(out, "claims.yml"), "utf-8")).claims;
    const c7 = claims.find((c: { id: string }) => c.id === "C7");
    expect(c7.validators).toHaveLength(2);
    expect(c7.validators[0].kind).toBe("attest");
    expect(c7.validators[1].gated_by).toBe("v_attest");
  });

  it("writes SHA256SUMS covering shipped files", () => {
    const out = scratch();
    writeSubmission(buildWorkedExample(), out, { stageFrom: FIXTURE_SRC });
    const sums = readFileSync(join(out, "SHA256SUMS"), "utf-8");
    expect(sums).toContain("manifest.yml");
    expect(sums).toContain("experiments/posterior_contraction/contraction.csv");
    expect(sums).not.toContain("SHA256SUMS");
  });
});

describe("schema conformance", () => {
  it("the emitted model validates against the canonical JSON Schema", () => {
    const schema = JSON.parse(readFileSync(SCHEMA, "utf-8"));
    const ajv = new Ajv({ strict: false, allErrors: true });
    const validate = ajv.compile(schema);
    const ok = validate(buildWorkedExample());
    if (!ok) console.error(validate.errors);
    expect(ok).toBe(true);
  });

  it("rejects empty or root-normalizing research-agent paths", () => {
    const schema = JSON.parse(readFileSync(SCHEMA, "utf-8"));
    const ajv = new Ajv({ strict: false, allErrors: true });
    const validate = ajv.compile(schema);
    for (const path of ["", ".", ".sdk", ".SDK", ".sdk/agent.md", ".SDK/agent.md", "foo/..", "foo/../agent.md", "../agent.md", "/agent.md", "C:/agent.md", "C:agent.md", "manifest.yml", "Manifest.yml", "claims.yml/agent.md"]) {
      const model = buildWorkedExample() as any;
      model.research_agent = { path, model: "m", grounding_sources: ["claims.yml"] };
      expect(validate(model)).toBe(false);
      expect(validate.errors?.some((e) => e.instancePath === "/research_agent/path")).toBe(true);
    }
  });

  it("rejects malformed research-agent model and grounding sources", () => {
    const schema = JSON.parse(readFileSync(SCHEMA, "utf-8"));
    const ajv = new Ajv({ strict: false, allErrors: true });
    const validate = ajv.compile(schema);
    for (const grounding_sources of [[""], ["   "], ["../outside.txt"], ["/abs.txt"], ["C:/secret"], ["C:secret"], ["foo/../bar.txt"], [".sdk"], [".SDK"], [".sdk/context.md"], [".SDK/context.md"], ["claims.yml/context.md"]]) {
      const model = buildWorkedExample() as any;
      model.research_agent = { path: "research-agent.md", model: "m", grounding_sources };
      expect(validate(model)).toBe(false);
      expect(validate.errors?.some((e) => e.instancePath === "/research_agent/grounding_sources/0")).toBe(true);
    }

    const model = buildWorkedExample() as any;
    model.research_agent = { path: "research-agent.md", model: "   ", grounding_sources: ["claims.yml"] };
    expect(validate(model)).toBe(false);
    expect(validate.errors?.some((e) => e.instancePath === "/research_agent/model")).toBe(true);
  });

  it("rejects blank or unsafe paper paths", () => {
    const schema = JSON.parse(readFileSync(SCHEMA, "utf-8"));
    const ajv = new Ajv({ strict: false, allErrors: true });
    const validate = ajv.compile(schema);
    for (const paper of [{ pdf: "" }, { pdf: "   " }, { source: "" }, { source: "   " }, { pdf: "../paper.pdf" }, { pdf: "..\\paper.pdf" }, { source: "C:paper.tex" }, { source: "\\abs\\paper.tex" }, { claims_export: "../claims.yml", source: "paper.tex" }, { references_export: "claims.yml", source: "paper.tex" }]) {
      const model = buildWorkedExample() as any;
      model.paper = paper;
      expect(validate(model)).toBe(false);
      expect(validate.errors?.some((e) => e.instancePath.startsWith("/paper/"))).toBe(true);
    }
  });

  it("rejects unsafe experiment directories", () => {
    const schema = JSON.parse(readFileSync(SCHEMA, "utf-8"));
    const ajv = new Ajv({ strict: false, allErrors: true });
    const validate = ajv.compile(schema);
    for (const directory of ["../escape", "claims.yml", "claims.yml/child", ".sdk", ".SDK/child", "C:agent"]) {
      const model = buildWorkedExample() as any;
      model.experiments[0].directory = directory;
      expect(validate(model)).toBe(false);
      expect(validate.errors?.some((e) => e.instancePath === "/experiments/0/directory")).toBe(true);
    }
  });

  it("rejects unsafe result evidence paths", () => {
    const schema = JSON.parse(readFileSync(SCHEMA, "utf-8"));
    const ajv = new Ajv({ strict: false, allErrors: true });
    const validate = ajv.compile(schema);
    for (const evidence of ["claims.yml", "claims.yml\\child", "..\\evidence.csv"]) {
      const model = buildWorkedExample() as any;
      model.results[0].evidence = evidence;
      expect(validate(model)).toBe(false);
      expect(validate.errors?.some((e) => e.instancePath === "/results/0/evidence")).toBe(true);
    }
  });
});

describe("structural validation (spec §7)", () => {
  it("rejects a dangling result→claim reference", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, { id: "R1", validates: ["NOPE"], evidence: "e.csv", kind: "metrics" });
    expect(() => writeSubmission(a, scratch())).toThrowError(/unknown claim 'NOPE'/);
  });

  it("rejects an external dataset without a checksum", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addDataset(a, {
      id: "d",
      // @ts-expect-error intentionally missing sha256
      location: { kind: "external", uri: "https://e/x.tar" },
    });
    expect(() => writeSubmission(a, scratch())).toThrowError(/requires a `sha256`/);
  });

  it("rejects a builtin validator whose input.result is dangling (audit A2)", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "e", kind: "metrics" });
    addClaim(a, {
      id: "C1",
      statement: "s",
      validator: {
        kind: "builtin",
        name: "monotonic",
        input: { result: "NOPE", series: ["a"] },
        params: { direction: "decreasing" },
      },
    });
    expect(() => writeSubmission(a, scratch())).toThrowError(/input.result.*unknown result 'NOPE'/);
  });

  it("rejects gated_by pointing at a non-attest validator", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "e", kind: "metrics" });
    addClaim(a, {
      id: "C1",
      statement: "s",
      validators: [
        { id: "v1", kind: "llm_judge", criteria: "c", inputs: ["R1"] },
        { id: "v2", kind: "llm_judge", gated_by: "v1", criteria: "c", inputs: ["R1"] },
      ],
    });
    expect(() => writeSubmission(a, scratch())).toThrowError(/must reference an attest validator/);
  });
});

describe("iteration (spec §4.1)", () => {
  it("add* is upsert-by-id (replace, not duplicate)", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, { id: "C1", statement: "first", validators: [] });
    addClaim(a, { id: "C1", statement: "second", validators: [] });
    expect(a.claims).toHaveLength(1);
    expect(a.claims[0].statement).toBe("second");
  });

  it("openSubmission round-trips a written submission", () => {
    const out = scratch();
    writeSubmission(buildWorkedExample(), out, { stageFrom: FIXTURE_SRC });
    const reopened = openSubmission(out);
    expect(reopened.id).toBe("expt-42");
    expect(reopened.claims.map((c) => c.id).sort()).toEqual(["C1", "C7"]);
    expect(reopened.results.map((r) => r.id).sort()).toEqual(["R1", "R2"]);
    expect(reopened.traces).toHaveLength(1);
    // re-emitting the reopened artifact preserves authored blobs
    const report = writeSubmission(reopened, out);
    expect(report.ok).toBe(true);
    expect(existsSync(join(out, "data/interviews/P07.txt"))).toBe(true);
  });
});
