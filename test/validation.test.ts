import { describe, expect, it } from "vitest";

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
  validateStructure,
} from "../src/index.js";

/** Convenience: run structural validation and return the report. */
function check(a: Artifact) {
  return validateStructure(a);
}

function findError(a: Artifact, re: RegExp): boolean {
  return check(a).errors.some((e) => re.test(`${e.path}: ${e.message}`));
}
function findWarning(a: Artifact, re: RegExp): boolean {
  return check(a).warnings.some((w) => re.test(`${w.path}: ${w.message}`));
}

describe("dataset validation (spec §2.7)", () => {
  it("flags in_container without in_environment (error) and without env (warning)", () => {
    const a = createArtifact({ id: "x", title: "t" });
    // @ts-expect-error missing in_environment
    addDataset(a, { id: "d", location: { kind: "in_container", path: "/opt/data" } });
    expect(findError(a, /in_container dataset requires `in_environment`/)).toBe(true);
  });

  it("warns when an in_container dataset has no declared environment", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addDataset(a, {
      id: "d",
      location: { kind: "in_container", path: "/opt/data", in_environment: "primary" },
    });
    expect(findWarning(a, /in_container dataset but no environment declared/)).toBe(true);
  });

  it("accepts in_container when the environment exists", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addEnvironment(a, { name: "primary", image: { reference: "img:1" } });
    addDataset(a, {
      id: "d",
      location: { kind: "in_container", path: "/opt/data", in_environment: "primary" },
    });
    expect(check(a).ok).toBe(true);
  });

  it("rejects a dataset without a location kind", () => {
    const a = createArtifact({ id: "x", title: "t" });
    // @ts-expect-error missing location
    addDataset(a, { id: "d", location: {} });
    expect(findError(a, /dataset requires `location.kind`/)).toBe(true);
  });
});

describe("experiment validation (spec §2.2)", () => {
  it("requires directory and run.command", () => {
    const a = createArtifact({ id: "x", title: "t" });
    // @ts-expect-error missing directory + run
    addExperiment(a, { slug: "e1" });
    const report = check(a);
    expect(report.errors.some((e) => /requires `directory`/.test(e.message))).toBe(true);
    expect(report.errors.some((e) => /requires `run.command`/.test(e.message))).toBe(true);
  });

  it("flags uses_data → unknown dataset, depends_on → unknown experiment, runs_in → unknown env", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addEnvironment(a, { name: "primary", image: { reference: "img:1" } });
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "run" },
      uses_data: [{ dataset: "ghost", at: "data/x" }],
      depends_on: ["missing"],
      runs_in: "not-primary",
    });
    expect(findError(a, /references unknown dataset 'ghost'/)).toBe(true);
    expect(findError(a, /references unknown experiment 'missing'/)).toBe(true);
    expect(findError(a, /references unknown environment 'not-primary'/)).toBe(true);
  });
});

describe("trace validation (spec §2.2.1)", () => {
  it("flags a covers → unknown experiment", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addTrace(a, { id: "T1", kind: "agent_session", path: "traces/t.jsonl", covers: ["ghost"] });
    expect(findError(a, /trace\[T1\].covers: references unknown experiment 'ghost'/)).toBe(true);
  });

  it("requires id and path", () => {
    const a = createArtifact({ id: "x", title: "t" });
    // @ts-expect-error missing path
    addTrace(a, { id: "", kind: "agent_session" });
    const report = check(a);
    expect(report.ok).toBe(false);
  });

  it("accepts a human_interaction (HITL) trace — a non-run log the evaluator excludes from run dimensions", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addTrace(a, {
      id: "human-in-the-loop",
      kind: "human_interaction",
      path: "traces/human_interactions.md",
      counters: { entries: 3, clarifications: 1, gates: 2, revisions: 1 },
    });
    const report = check(a);
    expect(report.ok).toBe(true);
    expect(a.traces[0].kind).toBe("human_interaction");
  });
});

describe("result validation (spec §2.3)", () => {
  it("rejects an illegal validation_mode and an unknown produced_by", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, {
      id: "R1",
      validates: [],
      evidence: "e",
      kind: "metrics",
      // @ts-expect-error illegal enum
      validation_mode: "reticulate",
      produced_by: "ghost",
    });
    expect(findError(a, /illegal validation_mode 'reticulate'/)).toBe(true);
    expect(findError(a, /produced_by: references unknown experiment 'ghost'/)).toBe(true);
  });

  it("requires id, evidence, and kind", () => {
    const a = createArtifact({ id: "x", title: "t" });
    // @ts-expect-error missing fields
    addResult(a, { id: "", validates: [] });
    expect(check(a).ok).toBe(false);
  });
});

describe("validator well-formedness (spec §3)", () => {
  function claimWith(v: unknown) {
    const a = createArtifact({ id: "x", title: "t" });
    // @ts-expect-error deliberately malformed validators under test
    addClaim(a, { id: "C1", statement: "s", validators: [v] });
    return a;
  }

  it("builtin requires name", () => {
    expect(findError(claimWith({ kind: "builtin" }), /builtin validator requires `name`/)).toBe(true);
  });
  it("procedure requires instructions", () => {
    expect(
      findError(claimWith({ kind: "procedure" }), /procedure validator requires `instructions`/),
    ).toBe(true);
  });
  it("attest requires checks", () => {
    expect(findError(claimWith({ kind: "attest" }), /attest validator requires `checks`/)).toBe(true);
  });
  it("llm_judge requires criteria", () => {
    expect(
      findError(claimWith({ kind: "llm_judge" }), /llm_judge validator requires `criteria`/),
    ).toBe(true);
  });
  it("rejects an unknown validator kind", () => {
    expect(findError(claimWith({ kind: "wat" }), /unknown validator kind wat/)).toBe(true);
  });
});

describe("claim + gated_by validation (spec §2.4, §3.5)", () => {
  it("warns on a claim with no validators", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, { id: "C1", statement: "s", validators: [] });
    expect(findWarning(a, /claim has no validator/)).toBe(true);
    expect(check(a).ok).toBe(true); // a warning, not an error
  });

  it("flags gated_by → unknown validator id on the same claim", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "e", kind: "transcript" });
    addClaim(a, {
      id: "C1",
      statement: "s",
      validators: [
        { id: "v_inspect", kind: "llm_judge", gated_by: "ghost", criteria: "c", inputs: ["R1"] },
      ],
    });
    expect(findError(a, /references unknown validator 'ghost' on this claim/)).toBe(true);
  });

  it("accepts a well-formed attest-gates-inspect pair", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "e", kind: "transcript" });
    addClaim(a, {
      id: "C1",
      statement: "s",
      validators: [
        { id: "v_attest", kind: "attest", checks: "provenance", inputs: ["R1"] },
        { id: "v_inspect", kind: "llm_judge", gated_by: "v_attest", criteria: "c", inputs: ["R1"] },
      ],
    });
    expect(check(a).ok).toBe(true);
  });

  it("flags a procedure/attest/llm_judge inputs[] → unknown result", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, {
      id: "C1",
      statement: "s",
      validators: [{ id: "v", kind: "attest", checks: "integrity", inputs: ["R_ghost"] }],
    });
    expect(findError(a, /inputs: references unknown result 'R_ghost'/)).toBe(true);
  });
});

describe("assessment validation (spec §2.1.1)", () => {
  it("requires dimension and a legal scope", () => {
    const a = createArtifact({ id: "x", title: "t" });
    // @ts-expect-error illegal scope + missing dimension
    a.assessments.push({ id: "A1", scope: "galaxy" });
    const report = check(a);
    expect(report.errors.some((e) => /requires `dimension`/.test(e.message))).toBe(true);
    expect(report.errors.some((e) => /scope must be 'artifact' or 'paper'/.test(e.message))).toBe(
      true,
    );
  });
});

describe("artifact root validation", () => {
  it("requires id and title on the artifact", () => {
    const a = createArtifact({ id: "x", title: "t" });
    a.id = "";
    a.title = "";
    const report = check(a);
    expect(report.errors.some((e) => /artifact.id/.test(e.path))).toBe(true);
    expect(report.errors.some((e) => /artifact.title/.test(e.path))).toBe(true);
  });
});

describe("environment image digest pinning (spec §2.5)", () => {
  it("warns when a run image is declared with a bare tag and no digest", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addEnvironment(a, { name: "primary", image: { reference: "registry/artifact:1.2" } });
    expect(findWarning(a, /image is not pinned to a digest/)).toBe(true);
    // A warning is not an error — emission is not blocked.
    expect(check(a).ok).toBe(true);
  });

  it("does not warn when image.digest is set", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addEnvironment(a, {
      name: "primary",
      image: { reference: "registry/artifact:1.2", digest: `sha256:${"a".repeat(64)}` },
    });
    expect(findWarning(a, /image is not pinned to a digest/)).toBe(false);
  });

  it("does not warn when the reference already embeds a digest", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addEnvironment(a, {
      name: "primary",
      image: { reference: `registry/artifact:1.2@sha256:${"b".repeat(64)}` },
    });
    expect(findWarning(a, /image is not pinned to a digest/)).toBe(false);
  });
});

describe("paper validation (spec §2.6 — pdf and/or source)", () => {
  it("accepts a paper with pdf only", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachPaper(a, { pdf: "paper.pdf" });
    expect(findError(a, /paper requires at least one/)).toBe(false);
  });

  it("accepts a paper with source only (e.g. uncompiled LaTeX)", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachPaper(a, { source: "paper/" });
    expect(findError(a, /paper requires at least one/)).toBe(false);
  });

  it("accepts a paper with both pdf and source", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachPaper(a, { pdf: "paper.pdf", source: "paper/" });
    expect(findError(a, /paper requires at least one/)).toBe(false);
  });

  it("rejects a paper block with neither pdf nor source", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachPaper(a, {});
    expect(findError(a, /paper requires at least one of `pdf` or `source`/)).toBe(true);
  });

  it("rejects whitespace-only paper paths", () => {
    for (const paper of [{ pdf: "   " }, { source: "   " }]) {
      const a = createArtifact({ id: "x", title: "t" });
      attachPaper(a, paper);
      expect(findError(a, /paper requires at least one of `pdf` or `source`/)).toBe(true);
    }
  });
});
