import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, describe, expect, it } from "vitest";

import {
  Artifact,
  addClaim,
  addExperiment,
  createArtifact,
  failExperiment,
  getClaim,
  openSubmission,
  validateStructure,
  writeSubmission,
} from "../src/index.js";

const tmpDirs: string[] = [];
function scratch(): string {
  const d = mkdtempSync(join(tmpdir(), "uas-stance-"));
  tmpDirs.push(d);
  return d;
}
afterAll(() => {
  for (const d of tmpDirs) rmSync(d, { recursive: true, force: true });
});

function findError(a: Artifact, re: RegExp): boolean {
  return validateStructure(a).errors.some((e) =>
    re.test(`${e.path}: ${e.message}`),
  );
}
function findWarning(a: Artifact, re: RegExp): boolean {
  return validateStructure(a).warnings.some((w) =>
    re.test(`${w.path}: ${w.message}`),
  );
}

describe("claim stance (spec §2.4.1)", () => {
  it("defaults to undefined stance (≡ finding) for a plain claim", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, {
      id: "c1",
      statement: "s",
      validator: { kind: "attest", checks: "integrity" },
    });
    expect(getClaim(a, "c1")!.stance).toBeUndefined();
  });

  it("records an explicit hypothesis stance and tested_by", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addExperiment(a, { slug: "e1", directory: "d", run: { command: "r" } });
    addClaim(a, {
      id: "h1",
      statement: "caching helps",
      stance: "hypothesis",
      tested_by: ["e1"],
    });
    const c = getClaim(a, "h1")!;
    expect(c.stance).toBe("hypothesis");
    expect(c.tested_by).toEqual(["e1"]);
  });

  it("does NOT warn 'unverifiable' for a hypothesis with no validator", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, { id: "h1", statement: "s", stance: "hypothesis" });
    expect(findWarning(a, /claim\[h1\].*no validator/)).toBe(false);
  });

  it("still warns 'unverifiable' for a finding with no validator", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, { id: "c1", statement: "s" });
    expect(findWarning(a, /claim\[c1\].*no validator/)).toBe(true);
  });

  it("errors on an illegal stance value", () => {
    const a = createArtifact({ id: "x", title: "t" });
    // @ts-expect-error invalid stance
    addClaim(a, { id: "c1", statement: "s", stance: "guess" });
    expect(findError(a, /claim\[c1\]\.stance: invalid stance/)).toBe(true);
  });

  it("errors when tested_by references an unknown experiment", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addClaim(a, {
      id: "h1",
      statement: "s",
      stance: "hypothesis",
      tested_by: ["nope"],
    });
    expect(
      findError(
        a,
        /claim\[h1\]\.tested_by: references unknown experiment 'nope'/,
      ),
    ).toBe(true);
  });

  it("supports the hypothesis→finding lifecycle via upsert", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addExperiment(a, { slug: "e1", directory: "d", run: { command: "r" } });
    addClaim(a, {
      id: "h1",
      statement: "s",
      stance: "hypothesis",
      tested_by: ["e1"],
    });
    addClaim(
      a,
      {
        id: "h1",
        statement: "s",
        stance: "finding",
        tested_by: ["e1"],
        validator: { kind: "attest", checks: "integrity" },
      },
      { actor: "writer", rationale: "e1 supported the hypothesis" },
    );
    expect(getClaim(a, "h1")!.stance).toBe("finding");
    // the promotion is journaled (a `replace` op on the claim)
    expect(
      a.journal.some((e) => e.target.kind === "claim" && e.op === "replace"),
    ).toBe(true);
  });

  it("keeps a refuted hypothesis as a preserved negative result", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addExperiment(a, { slug: "e1", directory: "d", run: { command: "r" } });
    addClaim(a, {
      id: "h1",
      statement: "s",
      stance: "hypothesis",
      tested_by: ["e1"],
    });
    failExperiment(
      a,
      "e1",
      { stage: "analysis", summary: "no effect" },
      { rationale: "flat within noise" },
    );
    expect(getClaim(a, "h1")!.stance).toBe("hypothesis");
    const exp = a.experiments.find((e) => e.slug === "e1")!;
    expect(exp.disposition?.status).toBe("failed");
  });

  it("round-trips stance + tested_by through write/open", () => {
    const a = createArtifact({ id: "x", title: "t" });
    addExperiment(a, { slug: "e1", directory: "d", run: { command: "r" } });
    addClaim(a, {
      id: "h1",
      statement: "s",
      stance: "hypothesis",
      tested_by: ["e1"],
    });
    const dir = scratch();
    writeSubmission(a, dir);
    const reopened = openSubmission(dir);
    const c = reopened.claims.find((x) => x.id === "h1")!;
    expect(c.stance).toBe("hypothesis");
    expect(c.tested_by).toEqual(["e1"]);
  });
});
