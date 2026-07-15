import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, describe, expect, it } from "vitest";
import { parse } from "yaml";

import {
  Artifact,
  attachResearchAgent,
  configureJournal,
  createArtifact,
  listJournal,
  openSubmission,
  validateStructure,
  writeSubmission,
} from "../src/index.js";

const tmpDirs: string[] = [];
function scratch(): string {
  const d = mkdtempSync(join(tmpdir(), "uas-agent-"));
  tmpDirs.push(d);
  return d;
}
afterAll(() => {
  for (const d of tmpDirs) rmSync(d, { recursive: true, force: true });
});

const FIXED = "2026-01-01T00:00:00.000Z";
function seeded(): Artifact {
  const a = createArtifact({ id: "x", title: "t" });
  configureJournal(a, { actor: "agent:experiment", now: () => FIXED });
  return a;
}

describe("research agent element (spec §2.9)", () => {
  it("is optional and absent by default — clean validation, inventory flag false", () => {
    const a = createArtifact({ id: "x", title: "t" });
    expect(a.research_agent).toBeUndefined();
    expect(validateStructure(a).ok).toBe(true);

    const out = scratch();
    writeSubmission(a, out);
    const manifest = parse(readFileSync(join(out, "manifest.yml"), "utf-8"));
    expect(manifest.research_agent).toBeUndefined();
    expect(manifest.evidence_inventory.has_research_agent).toBe(false);
  });

  it("attaches with a pinned model + grounding sources, defaulting the path", () => {
    const a = seeded();
    const agent = attachResearchAgent(a, {
      path: "",
      model: "copilot/gpt-5.5@2026-06-01",
      grounding_sources: ["claims.yml", "results.yml"],
      scope: ["research", "negative-results"],
    });
    expect(agent.path).toBe("research-agent.md");
    expect(a.research_agent?.model).toBe("copilot/gpt-5.5@2026-06-01");
    expect(validateStructure(a).ok).toBe(true);
  });

  it("journals the attach with a target of kind research_agent", () => {
    const a = seeded();
    attachResearchAgent(
      a,
      { path: "research-agent.md", model: "m", grounding_sources: ["claims.yml"] },
      { rationale: "ship the witness" },
    );
    const entry = listJournal(a).at(-1)!;
    expect(entry.op).toBe("attach");
    expect(entry.target).toEqual({ kind: "research_agent", id: "research-agent.md" });
    expect(entry.rationale).toBe("ship the witness");
  });

  it("round-trips through serialize → manifest → open, staging the prose file", () => {
    const src = scratch();
    writeFileSync(join(src, "research-agent.md"), "# persona\nask me anything", "utf-8");
    const a = seeded();
    attachResearchAgent(a, {
      path: "research-agent.md",
      model: "copilot/gpt-5.5@2026-06-01",
      grounding_sources: ["claims.yml", "paper/"],
      scope: ["results"],
    });

    const out = scratch();
    writeSubmission(a, out, { stageFrom: src });

    const manifest = parse(readFileSync(join(out, "manifest.yml"), "utf-8"));
    expect(manifest.research_agent.model).toBe("copilot/gpt-5.5@2026-06-01");
    expect(manifest.research_agent.grounding_sources).toEqual(["claims.yml", "paper/"]);
    expect(manifest.evidence_inventory.has_research_agent).toBe(true);
    expect(readFileSync(join(out, "research-agent.md"), "utf-8")).toContain("persona");

    const reopened = openSubmission(out);
    expect(reopened.research_agent).toEqual(a.research_agent);
  });

  it("stages grounding source files with the persona", () => {
    const src = scratch();
    writeFileSync(join(src, "research-agent.md"), "# persona", "utf-8");
    mkdirSync(join(src, "agent"), { recursive: true });
    writeFileSync(join(src, "agent", "context.md"), "context", "utf-8");
    const a = seeded();
    attachResearchAgent(a, {
      path: "research-agent.md",
      model: "m",
      grounding_sources: ["agent/context.md"],
    });

    const out = scratch();
    const report = writeSubmission(a, out, { stageFrom: src });
    expect(report.missingBlobs).toEqual([]);
    expect(existsSync(join(out, "agent", "context.md"))).toBe(true);
    expect(readFileSync(join(out, "SHA256SUMS"), "utf-8")).toContain("agent/context.md");
  });


  it("requires a path to the authored persona file", () => {
    const a = seeded();
    (a as any).research_agent = { model: "m", grounding_sources: ["claims.yml"] };
    const report = validateStructure(a);
    expect(report.ok).toBe(false);
    expect(report.errors.some((e) => /research_agent.path/.test(e.path))).toBe(true);
    expect(() => writeSubmission(a, scratch())).toThrowError(/research_agent.path/);
  });

  it("rejects research-agent paths that are not plain relative file paths", () => {
    for (const path of [123, ".", ".sdk", ".SDK", ".sdk/agent.md", ".SDK/agent.md", "foo/..", "foo/../research-agent.md", "/abs-agent.md", "C:/agent.md", "C:agent.md", "manifest.yml", "Manifest.yml", "claims.yml/agent.md"]) {
      const a = seeded();
      (a as any).research_agent = { path, model: "m", grounding_sources: ["claims.yml"] };
      const report = validateStructure(a);
      expect(report.ok).toBe(false);
      expect(report.errors.some((e) => /research_agent.path/.test(e.path))).toBe(true);
      expect(() => writeSubmission(a, scratch(), { stageFrom: scratch() })).toThrowError(/research_agent.path/);
    }
  });

  it("requires grounding sources to be artifact-relative non-empty strings", () => {
    for (const grounding_sources of [[123], [""], ["   "], ["../outside.txt"], ["/abs.txt"], ["C:/secret"], ["C:secret"], ["foo/../bar.txt"], [".sdk"], [".SDK"], [".sdk/context.md"], [".SDK/context.md"], ["claims.yml/context.md"]]) {
      const a = seeded();
      (a as any).research_agent = { path: "research-agent.md", model: "m", grounding_sources };
      const report = validateStructure(a);
      expect(report.ok).toBe(false);
      expect(report.errors.some((e) => /research_agent\.grounding_sources\[0\]/.test(e.path))).toBe(true);
      expect(() => writeSubmission(a, scratch())).toThrowError(/grounding_source/);
    }
  });
  it("requires a pinned model", () => {
    for (const model of ["", "   ", 123]) {
      const a = seeded();
      (a as any).research_agent = { path: "research-agent.md", model, grounding_sources: ["claims.yml"] };
      const report = validateStructure(a);
      expect(report.ok).toBe(false);
      expect(report.errors.some((e) => /research_agent.model/.test(e.path))).toBe(true);
    }
  });

  it("requires at least one grounding source", () => {
    const a = seeded();
    attachResearchAgent(a, { path: "research-agent.md", model: "m", grounding_sources: [] });
    const report = validateStructure(a);
    expect(report.ok).toBe(false);
    expect(report.errors.some((e) => /research_agent.grounding_sources/.test(e.path))).toBe(true);
  });
});
