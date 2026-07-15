import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, describe, expect, it } from "vitest";
import { parse } from "yaml";

import {
  Artifact,
  abandonExperiment,
  addClaim,
  addExperiment,
  configureJournal,
  createArtifact,
  failExperiment,
  listAbandonedExperiments,
  listExperiments,
  listJournal,
  openSubmission,
  purgeExperiment,
  removeExperiment,
  supersedeExperiment,
  validateStructure,
  writeSubmission,
} from "../src/index.js";

const tmpDirs: string[] = [];
function scratch(): string {
  const d = mkdtempSync(join(tmpdir(), "uas-journal-"));
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

describe("journal records every mutation (spec §2.8)", () => {
  it("stamps seq, timestamp, actor, op, target and rationale", () => {
    const a = seeded();
    addExperiment(
      a,
      { slug: "e1", directory: "experiments/e1", run: { command: "run" } },
      {
        rationale: "first attempt at the sweep",
      },
    );
    const [entry] = listJournal(a);
    expect(entry.seq).toBe(1);
    expect(entry.timestamp).toBe(FIXED);
    expect(entry.actor).toBe("agent:experiment");
    expect(entry.op).toBe("add");
    expect(entry.target).toEqual({ kind: "experiment", id: "e1" });
    expect(entry.rationale).toBe("first attempt at the sweep");
    expect(entry.after).toBeDefined();
  });

  it("records a replace (with before/after) when an id is re-added", () => {
    const a = seeded();
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "v1" },
    });
    addExperiment(
      a,
      { slug: "e1", directory: "experiments/e1", run: { command: "v2" } },
      {
        rationale: "tuned the command",
      },
    );
    const j = listJournal(a);
    expect(j).toHaveLength(2);
    expect(j[1].op).toBe("replace");
    expect((j[1].before as { run: { command: string } }).run.command).toBe(
      "v1",
    );
    expect((j[1].after as { run: { command: string } }).run.command).toBe("v2");
  });

  it("ctx.actor overrides the configured default", () => {
    const a = seeded();
    addClaim(
      a,
      { id: "c1", statement: "s" },
      { actor: "human:reviewer", rationale: "authored" },
    );
    expect(listJournal(a)[0].actor).toBe("human:reviewer");
  });
});

describe("rationale elicitation policy (spec §4.2)", () => {
  it("policy 'required' throws when a mutation omits a rationale", () => {
    const a = createArtifact({ id: "x", title: "t" });
    configureJournal(a, { policy: "required" });
    expect(() =>
      addExperiment(a, { slug: "e1", directory: "d", run: { command: "r" } }),
    ).toThrowError(/rationale is required/);
    expect(listExperiments(a)).toHaveLength(0); // nothing committed before the throw? add ran first
  });

  it("policy 'prompt' asks the callback for a missing rationale", () => {
    const a = createArtifact({ id: "x", title: "t" });
    const seen: string[] = [];
    configureJournal(a, {
      policy: "prompt",
      onMissingRationale: (c) => {
        seen.push(`${c.op}:${c.target.kind}`);
        return "because the agent said so";
      },
    });
    addExperiment(a, { slug: "e1", directory: "d", run: { command: "r" } });
    expect(seen).toEqual(["add:experiment"]);
    expect(listJournal(a)[0].rationale).toBe("because the agent said so");
  });

  it("policy 'warn' (default) records an empty rationale", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, { id: "c1", statement: "s" });
    expect(listJournal(a)[0].rationale).toBe("");
  });
});

describe("experiment lifecycle — soft-remove keeps what was tried (spec §2.2.2)", () => {
  it("removeExperiment tags the experiment abandoned and retains it", () => {
    const a = seeded();
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "r" },
    });
    expect(removeExperiment(a, "e1", { rationale: "confounded by seed" })).toBe(
      true,
    );
    expect(listExperiments(a)).toHaveLength(1); // retained
    const e = listExperiments(a)[0];
    expect(e.disposition?.status).toBe("abandoned");
    expect(e.disposition?.rationale).toBe("confounded by seed");
    expect(listAbandonedExperiments(a).map((x) => x.slug)).toEqual(["e1"]);
    expect(listJournal(a).at(-1)?.op).toBe("abandon");
  });

  it("removeExperiment returns false for an unknown slug", () => {
    const a = seeded();
    expect(removeExperiment(a, "nope")).toBe(false);
  });

  it("abandon/removeExperiment requires a rationale regardless of policy (spec §4.2)", () => {
    const a = seeded();
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "r" },
    });
    const before = listJournal(a).length;
    // default policy is "warn", but abandon is in the always-required set
    expect(() => removeExperiment(a, "e1")).toThrowError(
      /rationale is required/,
    );
    // the throw is transactional: the experiment is untouched and nothing is journaled
    expect(listExperiments(a)[0].disposition).toBeUndefined();
    expect(listJournal(a)).toHaveLength(before);
  });

  it("failExperiment requires a rationale and records the failure detail", () => {
    const a = seeded();
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "r" },
    });
    expect(() =>
      failExperiment(a, "e1", { stage: "run", summary: "OOM" }),
    ).toThrowError(/rationale is required/);
    failExperiment(
      a,
      "e1",
      { stage: "run", summary: "OOM" },
      { rationale: "ran out of memory" },
    );
    const e = listExperiments(a)[0];
    expect(e.disposition?.status).toBe("failed");
    expect(e.disposition?.failure).toEqual({ stage: "run", summary: "OOM" });
  });

  it("supersedeExperiment requires a rationale (non-active status; spec §2.2.2) and keeps the lineage", () => {
    const a = seeded();
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "r" },
    });
    addExperiment(a, {
      slug: "e2",
      directory: "experiments/e2",
      run: { command: "r2" },
    });
    const before = listJournal(a).length;
    // default policy is "warn", but supersede drops an experiment → rationale is always required
    expect(() => supersedeExperiment(a, "e1", "e2")).toThrowError(
      /rationale is required/,
    );
    // transactional: the experiment is untouched and nothing is journaled
    expect(a.experiments[0].disposition).toBeUndefined();
    expect(listJournal(a)).toHaveLength(before);

    supersedeExperiment(a, "e1", "e2", { rationale: "e2 fixes the leakage" });
    expect(a.experiments[0].disposition?.status).toBe("superseded");
    expect(a.experiments[0].disposition?.superseded_by).toBe("e2");
  });

  it("purgeExperiment hard-deletes and requires a rationale", () => {
    const a = seeded();
    addExperiment(a, {
      slug: "e1",
      directory: "experiments/e1",
      run: { command: "r" },
    });
    expect(() => purgeExperiment(a, "e1")).toThrowError(
      /rationale is required/,
    );
    expect(
      purgeExperiment(a, "e1", { rationale: "duplicate, never ran" }),
    ).toBe(true);
    expect(listExperiments(a)).toHaveLength(0);
    expect(listJournal(a).at(-1)?.op).toBe("remove");
  });
});

describe("validation of disposition + journal (spec §7)", () => {
  it("warns on a non-active disposition with no rationale", () => {
    const a = createArtifact({ id: "x", title: "t" });
    a.experiments.push({
      slug: "e1",
      directory: "d",
      run: { command: "r" },
      disposition: { status: "abandoned", rationale: "" },
    });
    const rep = validateStructure(a);
    expect(rep.ok).toBe(true); // warning, not error
    expect(
      rep.warnings.some((w) => /process record is incomplete/.test(w.message)),
    ).toBe(true);
  });

  it("errors when superseded_by points at an unknown experiment", () => {
    const a = createArtifact({ id: "x", title: "t" });
    a.experiments.push({
      slug: "e1",
      directory: "d",
      run: { command: "r" },
      disposition: {
        status: "superseded",
        rationale: "r",
        superseded_by: "ghost",
      },
    });
    const rep = validateStructure(a);
    expect(rep.ok).toBe(false);
    expect(
      rep.errors.some((e) => /unknown experiment 'ghost'/.test(e.message)),
    ).toBe(true);
  });

  it("warns on a journal entry with no rationale", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, {
      id: "c1",
      statement: "s",
      validator: { kind: "attest", checks: "integrity" },
    });
    const rep = validateStructure(a);
    expect(rep.warnings.some((w) => /has no rationale/.test(w.message))).toBe(
      true,
    );
  });
});

describe("serialization + round-trip (spec §5)", () => {
  it("writes journal.yml, a DISPOSITION.md marker, and reopens the journal", () => {
    const a = seeded();
    addExperiment(
      a,
      { slug: "e1", directory: "experiments/e1", run: { command: "r" } },
      {
        rationale: "baseline",
      },
    );
    addExperiment(
      a,
      { slug: "e2", directory: "experiments/e2", run: { command: "r2" } },
      {
        rationale: "variant",
      },
    );
    abandonExperiment(a, "e2", { rationale: "worse than baseline" });
    addClaim(
      a,
      { id: "c1", statement: "s", validators: [] },
      { rationale: "headline" },
    );

    const out = scratch();
    writeSubmission(a, out);

    // journal.yml present and indexed by the manifest
    expect(existsSync(join(out, "journal.yml"))).toBe(true);
    const manifest = parse(readFileSync(join(out, "manifest.yml"), "utf-8"));
    expect(manifest.paths.journal).toBe("journal.yml");

    // disposition marker only for the non-active experiment
    expect(existsSync(join(out, "experiments/e2/DISPOSITION.md"))).toBe(true);
    expect(existsSync(join(out, "experiments/e1/DISPOSITION.md"))).toBe(false);
    expect(
      readFileSync(join(out, "experiments/e2/DISPOSITION.md"), "utf-8"),
    ).toContain("worse than baseline");

    const reopened = openSubmission(out);
    expect(reopened.journal).toHaveLength(a.journal.length);
    expect(reopened.journal.at(-1)?.rationale).toBe("headline");
    expect(
      reopened.experiments.find((e) => e.slug === "e2")?.disposition?.status,
    ).toBe("abandoned");
  });

  it("emits no journal.yml for an artifact with no recorded mutations", () => {
    const a = createArtifact({ id: "x", title: "t" });
    const out = scratch();
    writeSubmission(a, out);
    expect(existsSync(join(out, "journal.yml"))).toBe(false);
  });
});
