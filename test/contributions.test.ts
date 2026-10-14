import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { afterEach, describe, expect, it } from "vitest";
import { parse } from "yaml";
import { Ajv } from "ajv";
import {
  addClaim, addContribution, Artifact, computeEvidenceInventory, configureJournal,
  Contribution, createArtifact, getContribution, listContributions, openSubmission,
  removeContribution, validateStructure, writeSubmission,
} from "../src/index.js";

const full = JSON.parse(readFileSync(new URL("../parity/cases/contributions-complete.json", import.meta.url), "utf-8")).artifact as Artifact;
const roots: string[] = [];
function root(): string {
  const dir = mkdtempSync(join(tmpdir(), "sdk-contributions-"));
  roots.push(dir);
  return dir;
}
function model(): Artifact {
  const a = createArtifact({ id: "artifact", title: "Candidate advances" });
  addClaim(a, { id: "C1", statement: "A tested hypothesis", stance: "hypothesis" }, { rationale: "declare" });
  return a;
}
function document(dir: string, file = "manifest.yml"): Record<string, any> {
  return parse(readFileSync(join(dir, file), "utf-8"));
}
afterEach(() => { for (const dir of roots.splice(0)) rmSync(dir, { recursive: true, force: true }); });

describe("contribution authoring", () => {
  it("upserts, edits, reads and journals without truncating IDs or changing claim ownership", () => {
    const a = model();
    const c = structuredClone(full.contributions![0]);
    configureJournal(a, { policy: "required", actor: "human:author", now: () => "2026-10-14T00:00:00Z" });
    addContribution(a, c, { rationale: "candidate" });
    addContribution(a, { ...c, statement: "Edited declaration" }, { rationale: "clarify" });
    expect(getContribution(a, c.id)?.statement).toBe("Edited declaration");
    expect(a.contributions).toHaveLength(1);
    const listed = listContributions(a);
    listed.pop();
    expect(a.contributions).toHaveLength(1);
    expect(a.journal.at(-1)).toMatchObject({
      op: "replace", target: { kind: "contribution", id: c.id },
      actor: "human:author", before: c, after: { ...c, statement: "Edited declaration" },
    });
    expect(() => removeContribution(a, c.id)).toThrow(/rationale/);
    expect(removeContribution(a, c.id, { rationale: "withdraw" })).toBe(true);
    expect(removeContribution(a, c.id)).toBe(false);
    expect(a.claims.map(c => c.id)).toEqual(["C1"]);
    expect(a.journal.at(-1)?.target).toEqual({ kind: "contribution", id: c.id });
  });

  it("keeps old artifact literals legal and rejected lazy mutations atomic", () => {
    const { contributions: _, ...legacy } = model();
    const old: Artifact = legacy;
    expect(validateStructure(old).ok).toBe(true);
    expect(computeEvidenceInventory(old)).toMatchObject({ has_contributions: false, contribution_count: 0 });
    configureJournal(old, { policy: "required" });
    expect(() => addContribution(old, { id: "N1", statement: "Draft" })).toThrow(/rationale/);
    expect(old.contributions).toBeUndefined();
    expect(listContributions(old)).toEqual([]);
    expect(getContribution(old, "N1")).toBeUndefined();
    expect(removeContribution(old, "N1")).toBe(false);
  });
});

describe("contribution persistence", () => {
  it("writes, opens, edits and reopens all fields and unknown extensions with stable IDs", () => {
    const dir = root();
    const a = structuredClone(full);
    const report = writeSubmission(a, dir, { stageFrom: new URL("../parity/fixtures", import.meta.url).pathname });
    expect(report.filesWritten).toContain("contributions.yml");
    expect(document(dir).paths.contributions).toBe("contributions.yml");
    expect(document(dir).evidence_inventory).toMatchObject({ has_contributions: true, contribution_count: 3 });
    const state = JSON.parse(readFileSync(join(dir, ".sdk/state.json"), "utf-8"));
    expect(state.generated_files).toContain("contributions.yml");
    expect(state.generated_hashes["contributions.yml"]).toMatch(/^[a-f0-9]{64}$/);
    expect(readFileSync(join(dir, "SHA256SUMS"), "utf-8")).toContain("  contributions.yml");
    const reopened = openSubmission(dir);
    expect(reopened.contributions).toEqual(a.contributions);
    const edited = { ...reopened.contributions![0], statement: "A refined candidate" };
    addContribution(reopened, edited, { rationale: "refine" });
    writeSubmission(reopened, dir);
    expect(openSubmission(dir).contributions).toEqual([edited, ...a.contributions!.slice(1)]);
  });

  it("removes unchanged generated empty indexes and never resurrects detached edited indexes", () => {
    const dir = root(), a = model();
    addContribution(a, { id: "N1", statement: "Draft" }, { rationale: "declare" });
    writeSubmission(a, dir);
    removeContribution(a, "N1", { rationale: "withdraw" });
    writeSubmission(a, dir);
    expect(existsSync(join(dir, "contributions.yml"))).toBe(false);
    expect(document(dir).paths).not.toHaveProperty("contributions");
    expect(openSubmission(dir).contributions ?? []).toEqual([]);
    addContribution(a, { id: "N2", statement: "Replacement" }, { rationale: "declare" });
    writeSubmission(a, dir);
    const authored = "contributions:\n  - id: external\n    statement: Edited externally\n";
    writeFileSync(join(dir, "contributions.yml"), authored, "utf-8");
    removeContribution(a, "N2", { rationale: "detach" });
    writeSubmission(a, dir);
    expect(readFileSync(join(dir, "contributions.yml"), "utf-8")).toBe(authored);
    expect(openSubmission(dir).contributions ?? []).toEqual([]);
    expect(JSON.parse(readFileSync(join(dir, ".sdk/state.json"), "utf-8")).authored_files).toHaveProperty("contributions.yml");
  });

  it("refuses accidental overwrites before changing manifest, then allows explicit reopen/edit", () => {
    const dir = root(), a = model();
    addContribution(a, { id: "N1", statement: "Draft" }, { rationale: "declare" });
    writeSubmission(a, dir);
    const before = readFileSync(join(dir, "manifest.yml"), "utf-8");
    const authored = "contributions:\n  - id: N1\n    statement: External edit\n    x_field: {keep: null}\n";
    writeFileSync(join(dir, "contributions.yml"), authored, "utf-8");
    expect(() => writeSubmission(a, dir)).toThrow(/Refusing to overwrite/);
    expect(readFileSync(join(dir, "manifest.yml"), "utf-8")).toBe(before);
    const reopened = openSubmission(dir);
    addContribution(reopened, { ...reopened.contributions![0], statement: "Intentional revision" }, { rationale: "revise" });
    writeSubmission(reopened, dir);
    expect(openSubmission(dir).contributions![0]).toMatchObject({ id: "N1", statement: "Intentional revision", x_field: { keep: null } });
    writeFileSync(join(dir, "contributions.yml"), authored, "utf-8");
    expect(() => writeSubmission(reopened, dir)).toThrow(/Refusing to overwrite/);
  });

  it("does not adopt an existing authored destination without an explicit open", () => {
    const dir = root(), a = model();
    writeFileSync(join(dir, "contributions.yml"), "authored notes", "utf-8");
    addContribution(a, { id: "N1", statement: "Draft" }, { rationale: "declare" });
    expect(() => writeSubmission(a, dir)).toThrow(/Refusing to overwrite/);
    expect(existsSync(join(dir, "manifest.yml"))).toBe(false);
  });

  it("opens relocated declarations and preserves their authored file on canonical rewrite/removal", () => {
    const dir = root();
    writeSubmission(model(), dir);
    mkdirSync(join(dir, "indexes"));
    writeFileSync(join(dir, "indexes/advances.yml"), "contributions:\n  - id: N1\n    statement: Draft\n", "utf-8");
    const manifest = readFileSync(join(dir, "manifest.yml"), "utf-8").replace("paths:\n", "paths:\n  contributions: indexes/advances.yml\n");
    writeFileSync(join(dir, "manifest.yml"), manifest, "utf-8");
    const a = openSubmission(dir);
    expect(a.contributions?.[0].id).toBe("N1");
    writeSubmission(a, dir);
    expect(document(dir).paths.contributions).toBe("contributions.yml");
    removeContribution(a, "N1", { rationale: "withdraw" });
    writeSubmission(a, dir);
    expect(existsSync(join(dir, "indexes/advances.yml"))).toBe(true);
  });

  it.each(["../outside.yml", "/absolute.yml", "C:outside.yml", "..\\outside.yml", ".sdk/state.json", "claims.yml", "contributions.yml/../claims.yml", "indexes//file.yml", ""] )("rejects unsafe declared path %j", (path) => {
    const dir = root();
    writeFileSync(join(dir, "manifest.yml"), JSON.stringify({ format_version: "evaluable-artifact/v3", id: "a", title: "a", paths: { contributions: path } }), "utf-8");
    expect(() => openSubmission(dir)).toThrow(/contributions index path/);
  });

  it("rejects symlinked input/output indexes and missing or malformed declared indexes", () => {
    const dir = root(), outside = root();
    const target = join(outside, "data.yml");
    writeFileSync(target, "contributions: []\n", "utf-8");
    symlinkSync(target, join(dir, "contributions.yml"));
    expect(() => writeSubmission(model(), dir)).toThrow(/symlink/);
    writeFileSync(join(dir, "manifest.yml"), JSON.stringify({ format_version: "evaluable-artifact/v3", paths: { contributions: "contributions.yml" } }), "utf-8");
    expect(() => openSubmission(dir)).toThrow(/symlink/);
    rmSync(join(dir, "contributions.yml"));
    expect(() => openSubmission(dir)).toThrow(/missing/);
    writeFileSync(join(dir, "contributions.yml"), "contributions: {}\n", "utf-8");
    expect(() => openSubmission(dir)).toThrow(/array/);
  });
});

describe("contribution structural validation and schema", () => {
  const schema = JSON.parse(readFileSync(new URL("../schema/evaluable-artifact-v3.schema.json", import.meta.url), "utf-8"));
  const schemaCheck = new Ajv({ strict: false }).compile(schema);
  it("accepts drafts with warnings, no merit or count constraints and many-to-many links", () => {
    const a = model();
    for (const c of [{ id: "N1", statement: "Draft" }, { id: "N2", statement: "Empty support", supporting_claims: [] }, { id: "N3", statement: "Supported", supporting_claims: ["C1"] }]) addContribution(a, c, { rationale: "declare" });
    const report = validateStructure(a);
    expect(report.ok).toBe(true);
    expect(report.warnings.map(w => w.path)).toEqual(["contribution[N1].supporting_claims", "contribution[N2].supporting_claims"]);
    expect(schemaCheck(a)).toBe(true);
  });

  it.each([
    {}, { id: "", statement: "Draft" }, { id: "N", statement: "  " },
    { id: "N", statement: "Draft", supporting_claims: ["C1", "C1"] },
    { id: "N", statement: "Draft", supporting_claims: "C1" },
    { id: "N", statement: "Draft", significance: { impact: "established" } },
    { id: "N", statement: "Draft", significance: { evidence: ["bare filename"] } },
    { id: "N", statement: "Draft", originality: { comparisons: [{ reference: "r" }] } },
    { id: "N", statement: "Draft", originality: { coverage: { sources: "search" } } },
    { id: "N", statement: "Draft", provenance: { kind: "evaluator-verdict" } },
    { id: "N", statement: "Draft", provenance: null },
    { id: "N", statement: "Draft", originality: { coverage: null } },
    { id: "N", statement: "Draft", paper_ref: { char_start: -1 } },
    null, 7, "declaration",
  ])("runtime and canonical schema reject malformed declaration %j", (c) => {
    const a = model();
    a.contributions = [c] as Contribution[];
    expect(validateStructure(a).ok).toBe(false);
    expect(schemaCheck(a)).toBe(false);
    const dir = join(root(), "unwritten");
    expect(() => writeSubmission(a, dir)).toThrow(/structural/);
    expect(existsSync(dir)).toBe(false);
  });

  it("diagnoses duplicate IDs, dangling claims/results and bibliography IDs without novelty judgments", () => {
    const a = model();
    a.contributions = [{ id: "N", statement: "First", supporting_claims: ["missing"], significance: { evidence: ["result:missing", "claim:missing", "reference:missing"] }, originality: { comparisons: [{ reference: "missing", distinction: "Different" }] } }, { id: "N", statement: "Duplicate" }];
    const report = validateStructure(a, { referenceIds: [] });
    expect(report.errors.map(i => i.path)).toEqual([
      "contribution[N].supporting_claims", "contribution[N].significance.evidence[0]", "contribution[N].significance.evidence[1]", "contribution[N].significance.evidence[2]", "contribution[N].originality.comparisons[0].reference", "contribution[N].id",
    ]);
  });

  it.each(["references.yml", "references.json", "references.bib"])("resolves existing bibliography IDs from %s and rejects known dangling references", (file) => {
    const dir = root(), source = root(), a = model();
    a.paper = { source: "paper.md", references_export: file };
    writeFileSync(join(source, "paper.md"), "Paper", "utf-8");
    writeFileSync(join(source, file), file.endsWith(".bib") ? "@article{existing, title={Prior work}}\n" : JSON.stringify({ references: [{ id: "existing" }] }), "utf-8");
    addContribution(a, { id: "N", statement: "Draft", originality: { comparisons: [{ reference: "existing", distinction: "A declared distinction" }] } }, { rationale: "declare" });
    expect(validateStructure(a).warnings.some(w => w.path.endsWith(".reference"))).toBe(true);
    expect(writeSubmission(a, dir, { stageFrom: source }).warnings.some(w => w.path.endsWith(".reference"))).toBe(false);
    a.contributions![0].originality!.comparisons![0].reference = "missing";
    expect(() => writeSubmission(a, dir)).toThrow(/unknown bibliography ID/);
  });

  it("reserves contributions.yml against authored blob collisions", () => {
    const a = model();
    a.paper = { pdf: "contributions.yml" };
    expect(validateStructure(a).errors.map(i => i.path)).toContain("paper.pdf");
  });

  it("accepts an explicitly empty declared index without preserving a stale path", () => {
    const dir = root();
    writeFileSync(join(dir, "manifest.yml"), JSON.stringify({ format_version: "evaluable-artifact/v3", id: "empty", title: "Empty", paths: { contributions: "contributions.yml" } }), "utf-8");
    writeFileSync(join(dir, "contributions.yml"), "contributions: []\n", "utf-8");
    const a = openSubmission(dir);
    expect(validateStructure(a).ok).toBe(true);
    writeSubmission(a, dir);
    expect(document(dir).paths).not.toHaveProperty("contributions");
    expect(openSubmission(dir).contributions ?? []).toEqual([]);
  });

  it("never treats BibTeX text inside an entry/comment as a separate bibliography identity", () => {
    const dir = root(), a = model();
    a.paper = { source: "paper.md", references_export: "refs.bib" };
    writeFileSync(join(dir, "paper.md"), "Paper", "utf-8");
    writeFileSync(join(dir, "refs.bib"), '@comment{ @article{fake, title={not an entry}} }\n@article{real, title={Text @book{also-fake, year={2020}}}}\n', "utf-8");
    addContribution(a, { id: "N", statement: "Draft", originality: { comparisons: [{ reference: "real", distinction: "Different" }] } }, { rationale: "declare" });
    expect(writeSubmission(a, dir).ok).toBe(true);
    a.contributions![0].originality!.comparisons![0].reference = "fake";
    expect(() => writeSubmission(a, dir)).toThrow(/unknown bibliography ID/);
  });

  it.each(["unrecognized export", "references: [", "references: [{title: unknown}]"])("keeps unavailable bibliography identity explicit for %j", (text) => {
    const dir = root(), a = model();
    a.paper = { source: "paper.md", references_export: "refs.yml" };
    writeFileSync(join(dir, "paper.md"), "Paper", "utf-8");
    writeFileSync(join(dir, "refs.yml"), text, "utf-8");
    addContribution(a, { id: "N", statement: "Draft", originality: { comparisons: [{ reference: "unknown", distinction: "Different" }] } }, { rationale: "declare" });
    expect(writeSubmission(a, dir).warnings.some(i => i.path.endsWith(".reference"))).toBe(true);
  });

  it("migrates v2 explicitly on write and retains the unchanged legacy schema", () => {
    const dir = root(), a = model();
    const oldSchema = JSON.parse(readFileSync(new URL("../schema/evaluable-artifact-v2.schema.json", import.meta.url), "utf-8"));
    a.format_version = "evaluable-artifact/v2";
    expect(new Ajv({ strict: false }).compile(oldSchema)(a)).toBe(true);
    writeFileSync(join(dir, "manifest.yml"), JSON.stringify({ format_version: a.format_version, id: "legacy", title: "Legacy" }), "utf-8");
    const legacy = openSubmission(dir);
    expect(legacy.format_version).toBe("evaluable-artifact/v2");
    writeSubmission(legacy, dir);
    expect(legacy.format_version).toBe("evaluable-artifact/v2"); // Caller object is not silently mutated.
    expect(openSubmission(dir).format_version).toBe("evaluable-artifact/v3");
    expect(new Ajv({ strict: false }).compile(oldSchema)(openSubmission(dir))).toBe(false);
    writeFileSync(join(dir, "manifest.yml"), "format_version: evaluable-artifact/v4\n", "utf-8");
    expect(() => openSubmission(dir)).toThrow(/unsupported format/);
  });
});
