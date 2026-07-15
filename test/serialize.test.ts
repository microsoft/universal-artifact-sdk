import { mkdirSync, mkdtempSync, readFileSync, existsSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, describe, expect, it } from "vitest";
import { parse } from "yaml";

import {
  addAssessment,
  abandonExperiment,
  addExperiment,
  addClaim,
  addResult,
  attachPaper,
  attachResearchAgent,
  createArtifact,
  openSubmission,
  setReflection,
  writeSubmission,
} from "../src/index.js";

const tmpDirs: string[] = [];
function scratch(): string {
  const d = mkdtempSync(join(tmpdir(), "uas-ser-"));
  tmpDirs.push(d);
  return d;
}
afterAll(() => {
  for (const d of tmpDirs) rmSync(d, { recursive: true, force: true });
});

describe("serialization edge cases (spec §5)", () => {
  it("writes assessments.yml when assessments are declared", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addAssessment(a, {
      id: "A1",
      dimension: "citation_integrity",
      scope: "paper",
      evidence: ["paper_references.yml"],
    });
    const out = scratch();
    writeSubmission(a, out);
    expect(existsSync(join(out, "assessments.yml"))).toBe(true);
    const doc = parse(readFileSync(join(out, "assessments.yml"), "utf-8"));
    expect(doc.assessments[0].dimension).toBe("citation_integrity");
    // manifest paths index should point at it
    const manifest = parse(readFileSync(join(out, "manifest.yml"), "utf-8"));
    expect(manifest.paths.assessments).toBe("assessments.yml");
  });

  it("omits traces.yml / assessments.yml when none are declared", () => {
    const a = createArtifact({ id: "x", title: "t" });
    const out = scratch();
    writeSubmission(a, out);
    expect(existsSync(join(out, "traces.yml"))).toBe(false);
    expect(existsSync(join(out, "assessments.yml"))).toBe(false);
  });

  it("writes reflection.md when reflection text is present", () => {
    const a = createArtifact({ id: "x", title: "t" });
    setReflection(a, "# limitations\nsmall sample.\n");
    const out = scratch();
    writeSubmission(a, out);
    expect(readFileSync(join(out, "reflection.md"), "utf-8")).toContain("small sample");
  });

  it("reports incomplete with a missing-blob warning when evidence is absent", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "evidence/never.csv", kind: "metrics" });
    addClaim(a, { id: "C1", statement: "s", validators: [] });
    const report = writeSubmission(a, scratch()); // no stageFrom → blob absent
    expect(report.incomplete).toBe(true);
    expect(report.missingBlobs).toContain("evidence/never.csv");
    expect(report.warnings.some((w) => /incomplete/.test(w.message))).toBe(true);
  });

  it("quiet mode suppresses the incomplete flag", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "evidence/never.csv", kind: "metrics" });
    addClaim(a, { id: "C1", statement: "s", validators: [] });
    const report = writeSubmission(a, scratch(), { quiet: true });
    expect(report.incomplete).toBe(false);
  });

  it("stageFrom reports blobs missing from the source root", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "evidence/absent.csv", kind: "metrics" });
    addClaim(a, { id: "C1", statement: "s", validators: [] });
    const emptySource = scratch();
    const report = writeSubmission(a, scratch(), { stageFrom: emptySource });
    expect(report.missingBlobs).toContain("evidence/absent.csv");
    expect(report.incomplete).toBe(true);
  });

  it("stageFrom reports missing current grounding sources even when stale output exists", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachResearchAgent(a, {
      path: "research-agent.md",
      model: "m",
      grounding_sources: ["agent/context.md"],
    });
    const src = scratch();
    writeFileSync(join(src, "research-agent.md"), "persona", "utf-8");
    const out = scratch();
    mkdirSync(join(out, "agent"), { recursive: true });
    writeFileSync(join(out, "agent", "context.md"), "stale", "utf-8");

    const report = writeSubmission(a, out, { stageFrom: src });
    expect(report.missingBlobs).toContain("agent/context.md");
    expect(report.incomplete).toBe(true);
    expect(report.warnings.some((w) => w.path === "blob[agent/context.md]")).toBe(true);
  });

  it("does not report exact generated grounding sources as missing under stageFrom", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachResearchAgent(a, {
      path: "research-agent.md",
      model: "m",
      grounding_sources: ["claims.yml", "Claims.yml"],
    });
    const src = scratch();
    writeFileSync(join(src, "research-agent.md"), "persona", "utf-8");
    const report = writeSubmission(a, scratch(), { stageFrom: src });
    expect(report.missingBlobs).not.toContain("claims.yml");
    expect(report.missingBlobs).not.toContain("Claims.yml");
    expect(report.warnings.some((w) => w.path === "blob[claims.yml]" || w.path === "blob[Claims.yml]")).toBe(false);
  });

  it("rejects invalid blob references before writing output", () => {
    for (const evidence of ["../outside.csv", "C:secret.csv", "claims.yml"]) {
      const a = createArtifact({ id: "x", title: "t" });
      addClaim(a, { id: "C1", statement: "s", validators: [] });
      addResult(a, { id: "R1", validates: ["C1"], evidence, kind: "metrics" });
      const out = scratch();
      expect(() => writeSubmission(a, out, { stageFrom: scratch() })).toThrowError(/result\[R1\]\.evidence/);
      expect(existsSync(join(out, "manifest.yml"))).toBe(false);
    }
  });

  it("rejects authored blob refs that collide with generated disposition markers", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addExperiment(a, { slug: "e", directory: "experiments/e", run: { command: "true" } });
    abandonExperiment(a, "e", { rationale: "not useful" });
    addClaim(a, { id: "C1", statement: "s", validators: [] });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "experiments/e/DISPOSITION.md", kind: "metrics" });

    expect(() => writeSubmission(a, scratch(), { stageFrom: scratch() })).toThrowError(/generated disposition marker/);
  });

  it("rejects disposition directories that shadow authored blob files", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachPaper(a, { pdf: "paper.pdf" });
    addExperiment(a, { slug: "paper", directory: "paper.pdf", run: { command: "true" } });
    abandonExperiment(a, "paper", { rationale: "not useful" });

    expect(() => writeSubmission(a, scratch())).toThrowError(/collides with authored blob paper\.pdf/);
  });

  it("records generated vs authored files in .sdk/state.json", () => {
    const a = createArtifact({ id: "x", title: "t" });
    const out = scratch();
    // an authored blob the producer placed directly into the output dir
    writeFileSync(join(out, "note.txt"), "hello", "utf-8");
    writeSubmission(a, out);
    const state = JSON.parse(readFileSync(join(out, ".sdk/state.json"), "utf-8"));
    expect(state.generated_files).toContain("manifest.yml");
    expect(state.generated_files).toContain("claims.yml");
    expect(Object.keys(state.authored_files)).toContain("note.txt");
    expect(state.generated_files).not.toContain("note.txt");
  });

  it("classifies staged producer blobs as authored, not generated (independent of stageFrom)", () => {
    // Regression: staged blobs used to be pushed onto the `written` (generated) index,
    // so authored_files came out empty and classification depended on invocation.
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, { id: "C1", statement: "s", validators: [] });
    addResult(a, { id: "R1", validates: ["C1"], evidence: "evidence/metrics.csv", kind: "metrics" });
    const src = scratch();
    mkdirSync(join(src, "evidence"), { recursive: true });
    writeFileSync(join(src, "evidence/metrics.csv"), "metric,value\nacc,0.9\n", "utf-8");
    const out = scratch();
    const report = writeSubmission(a, out, { stageFrom: src });
    expect(report.missingBlobs).toEqual([]);
    const state = JSON.parse(readFileSync(join(out, ".sdk/state.json"), "utf-8"));
    // the copied producer blob is authored (SDK can't reconstruct it) → never generated
    expect(Object.keys(state.authored_files)).toContain("evidence/metrics.csv");
    expect(state.generated_files).not.toContain("evidence/metrics.csv");
    // index files the SDK serializes from the model stay generated
    expect(state.generated_files).toContain("manifest.yml");
    expect(state.generated_files).toContain("results.yml");
    // but the staged blob is still reported among files written this run
    expect(report.filesWritten).toContain("evidence/metrics.csv");
  });

  it("rejects disposition marker paths outside the submission root", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addExperiment(a, {
      slug: "escape",
      directory: "../escape",
      run: { command: "true" },
    });
    abandonExperiment(a, "escape", { rationale: "not useful" });
    expect(() => writeSubmission(a, scratch())).toThrowError(
      /experiment\[escape\]\.directory/,
    );
  });

  it("rejects disposition marker paths in generated or internal SDK locations", () => {
    for (const directory of ["claims.yml", "claims.yml/child", ".sdk", ".SDK/child"]) {
      const a = createArtifact({ id: "x", title: "t" });
      addExperiment(a, { slug: "bad", directory, run: { command: "true" } });
      abandonExperiment(a, "bad", { rationale: "not useful" });
      expect(() => writeSubmission(a, scratch())).toThrowError(/experiment\[bad\]\.directory/);
    }
  });

  it("rejects staged research-agent paths outside the submission root", () => {
    const a = createArtifact({ id: "x", title: "t" });
    attachResearchAgent(a, {
      path: "../escaped-agent.md",
      model: "m",
      grounding_sources: ["claims.yml"],
    });
    expect(() => writeSubmission(a, scratch(), { stageFrom: scratch() })).toThrowError(
      /research_agent.path/,
    );
  });
});

describe("idempotency (spec §4.1)", () => {
  it("re-emitting an unchanged artifact produces identical index bytes", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, {
      id: "C1",
      statement: "s",
      validator: { kind: "attest", checks: "integrity" },
    });
    attachPaper(a, { pdf: "paper.pdf" });
    const out = scratch();

    writeSubmission(a, out);
    const first = {
      manifest: readFileSync(join(out, "manifest.yml"), "utf-8"),
      claims: readFileSync(join(out, "claims.yml"), "utf-8"),
      sums: readFileSync(join(out, "SHA256SUMS"), "utf-8"),
    };
    writeSubmission(a, out);
    const second = {
      manifest: readFileSync(join(out, "manifest.yml"), "utf-8"),
      claims: readFileSync(join(out, "claims.yml"), "utf-8"),
      sums: readFileSync(join(out, "SHA256SUMS"), "utf-8"),
    };
    expect(second).toEqual(first);
  });
});

describe("openSubmission edge cases (spec §4, §4.1)", () => {
  it("throws when there is no manifest.yml", () => {
    expect(() => openSubmission(scratch())).toThrowError(/no manifest.yml/);
  });

  it("reopens a minimal submission (no traces/assessments/paper)", () => {
    const a = createArtifact({ id: "min", title: "t" });
    addClaim(a, { id: "C1", statement: "s", validators: [] });
    const out = scratch();
    writeSubmission(a, out);
    const reopened = openSubmission(out);
    expect(reopened.id).toBe("min");
    expect(reopened.claims).toHaveLength(1);
    expect(reopened.traces).toEqual([]);
    expect(reopened.assessments).toEqual([]);
    expect(reopened.paper).toBeUndefined();
    expect(reopened.reflection).toBeUndefined();
  });

  it("round-trips reflection and paper through reopen", () => {
    const a = createArtifact({ id: "x", title: "t" });
    setReflection(a, "# reflection\n");
    attachPaper(a, { pdf: "paper.pdf", references_export: "paper_references.yml" });
    const out = scratch();
    writeSubmission(a, out);
    const reopened = openSubmission(out);
    expect(reopened.reflection).toContain("reflection");
    expect(reopened.paper?.references_export).toBe("paper_references.yml");
  });

  it("tolerates a hand-written manifest without a paths index (default filenames)", () => {
    const out = scratch();
    // an older/minimal manifest that omits `paths` and the sibling index files
    writeFileSync(
      join(out, "manifest.yml"),
      "format_version: evaluable-artifact/v2\nid: hand\ntitle: Hand-written\n",
      "utf-8",
    );
    const reopened = openSubmission(out);
    expect(reopened.id).toBe("hand");
    expect(reopened.title).toBe("Hand-written");
    expect(reopened.datasets).toEqual([]);
    expect(reopened.results).toEqual([]);
    expect(reopened.claims).toEqual([]);
  });
});
