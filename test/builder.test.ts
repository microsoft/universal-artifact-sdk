import { describe, expect, it } from "vitest";

import {
  Artifact,
  addAssessment,
  addClaim,
  addDataset,
  addEnvironment,
  addExperiment,
  addResult,
  addTrace,
  attachPaper,
  createArtifact,
  defaultValidationMode,
  getAssessment,
  getClaim,
  getDataset,
  getExperiment,
  getResult,
  getTrace,
  listAssessments,
  listClaims,
  listDatasets,
  listExperiments,
  listResults,
  listTraces,
  removeAssessment,
  removeClaim,
  removeDataset,
  removeExperiment,
  removeResult,
  removeTrace,
  setReflection,
} from "../src/index.js";

describe("createArtifact", () => {
  it("requires id and title", () => {
    // @ts-expect-error missing id
    expect(() => createArtifact({ title: "t" })).toThrowError(
      /`id` is required/,
    );
    // @ts-expect-error missing title
    expect(() => createArtifact({ id: "x" })).toThrowError(
      /`title` is required/,
    );
  });

  it("stamps the format and sdk versions and starts empty", () => {
    const a = createArtifact({
      id: "x",
      title: "t",
      producer: { name: "example-harness" },
    });
    expect(a.format_version).toBe("evaluable-artifact/v2");
    expect(a.sdk_version).toBe("artifact-sdk/v1");
    expect(a.producer).toEqual({ name: "example-harness" });
    expect(a.datasets).toEqual([]);
    expect(a.experiments).toEqual([]);
    expect(a.traces).toEqual([]);
    expect(a.results).toEqual([]);
    expect(a.claims).toEqual([]);
    expect(a.assessments).toEqual([]);
  });
});

describe("defaultValidationMode (spec §2.3)", () => {
  it("maps each kind to its default mode", () => {
    expect(defaultValidationMode("metrics")).toBe("re-analyze");
    expect(defaultValidationMode("table")).toBe("re-analyze");
    expect(defaultValidationMode("figure")).toBe("re-analyze");
    expect(defaultValidationMode("proof")).toBe("re-execute");
    expect(defaultValidationMode("log")).toBe("re-execute");
    expect(defaultValidationMode("external_reference")).toBe("attest");
    expect(defaultValidationMode("transcript")).toBe("inspect");
    expect(defaultValidationMode("survey")).toBe("inspect");
  });
});

describe("builder add/get/list/remove for every element", () => {
  function seeded(): Artifact {
    const a = createArtifact({ id: "x", title: "t" });
    addEnvironment(a, { name: "primary", image: { reference: "img:1" } });
    addDataset(a, {
      id: "d1",
      location: { kind: "in_artifact", path: "data/d1" },
    });
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "run" },
    });
    addTrace(a, { id: "t1", kind: "execution_log", path: "traces/t1.log" });
    addResult(a, { id: "r1", validates: [], evidence: "e", kind: "metrics" });
    addClaim(a, { id: "c1", statement: "s", validators: [] });
    addAssessment(a, {
      id: "a1",
      dimension: "citation_integrity",
      scope: "paper",
    });
    return a;
  }

  it("get returns the element; list returns a copy", () => {
    const a = seeded();
    expect(getDataset(a, "d1")?.id).toBe("d1");
    expect(getExperiment(a, "e1")?.slug).toBe("e1");
    expect(getTrace(a, "t1")?.id).toBe("t1");
    expect(getResult(a, "r1")?.id).toBe("r1");
    expect(getClaim(a, "c1")?.id).toBe("c1");
    expect(getAssessment(a, "a1")?.id).toBe("a1");

    const copy = listClaims(a);
    copy.push({ id: "zzz", statement: "x", validators: [] });
    expect(listClaims(a)).toHaveLength(1); // original untouched

    expect(listDatasets(a)).toHaveLength(1);
    expect(listExperiments(a)).toHaveLength(1);
    expect(listTraces(a)).toHaveLength(1);
    expect(listResults(a)).toHaveLength(1);
    expect(listAssessments(a)).toHaveLength(1);
  });

  it("remove deletes and returns true; false for unknown id", () => {
    const a = seeded();
    expect(removeDataset(a, "d1")).toBe(true);
    expect(removeDataset(a, "d1")).toBe(false);
    expect(removeExperiment(a, "e1", { rationale: "superseded by e2" })).toBe(
      true,
    );
    expect(removeTrace(a, "t1")).toBe(true);
    expect(removeResult(a, "r1")).toBe(true);
    expect(removeClaim(a, "c1")).toBe(true);
    expect(removeAssessment(a, "a1")).toBe(true);
    expect(removeAssessment(a, "nope")).toBe(false);
    expect(a.datasets).toHaveLength(0);
  });

  it("upsert-by-id replaces every element type in place", () => {
    const a = seeded();
    addDataset(a, {
      id: "d1",
      location: { kind: "in_artifact", path: "data/renamed" },
    });
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "run2" },
    });
    addTrace(a, { id: "t1", kind: "notebook", path: "traces/t1.ipynb" });
    addResult(a, { id: "r1", validates: [], evidence: "e2", kind: "figure" });
    addAssessment(a, {
      id: "a1",
      dimension: "execution_authenticity",
      scope: "artifact",
    });
    expect(a.datasets).toHaveLength(1);
    expect((getDataset(a, "d1")!.location as { path: string }).path).toBe(
      "data/renamed",
    );
    expect(getExperiment(a, "e1")!.run.command).toBe("run2");
    expect(getTrace(a, "t1")!.kind).toBe("notebook");
    expect(getResult(a, "r1")!.kind).toBe("figure");
    expect(getAssessment(a, "a1")!.dimension).toBe("execution_authenticity");
  });
});

describe("addClaim validator sugar (spec §2.4)", () => {
  it("accepts singular `validator` as a one-element list", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, {
      id: "c1",
      statement: "s",
      validator: { kind: "attest", checks: "integrity" },
    });
    expect(getClaim(a, "c1")!.validators).toHaveLength(1);
    expect(getClaim(a, "c1")!.validators[0].kind).toBe("attest");
  });

  it("defaults to an empty validator list when neither is given", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, { id: "c1", statement: "s" });
    expect(getClaim(a, "c1")!.validators).toEqual([]);
  });
});

describe("attachPaper / setReflection", () => {
  it("stores the paper and reflection on the artifact", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachPaper(a, { pdf: "paper.pdf", source: "paper/" });
    setReflection(a, "# limitations\n");
    expect(a.paper?.pdf).toBe("paper.pdf");
    expect(a.reflection).toBe("# limitations\n");
  });
});

describe("addEnvironment digest auto-fill (spec §2.5)", () => {
  it("lifts a digest embedded in the reference into image.digest", () => {
    const a = createArtifact({ id: "x", title: "t" });
    const digest = `sha256:${"c".repeat(64)}`;
    addEnvironment(a, { name: "primary", image: { reference: `registry/artifact:1.2@${digest}` } });
    expect(a.environment?.image.digest).toBe(digest);
  });

  it("leaves an explicit digest untouched and never invents one for a bare tag", () => {
    const a = createArtifact({ id: "x", title: "t" });
    const explicit = `sha256:${"d".repeat(64)}`;
    addEnvironment(a, {
      name: "primary",
      image: { reference: "registry/artifact:1.2@sha256:" + "e".repeat(64), digest: explicit },
    });
    expect(a.environment?.image.digest).toBe(explicit); // caller's digest wins

    const b = createArtifact({ id: "y", title: "t" });
    addEnvironment(b, { name: "primary", image: { reference: "registry/artifact:1.2" } });
    expect(b.environment?.image.digest).toBeUndefined(); // bare tag stays unpinned
  });
});
