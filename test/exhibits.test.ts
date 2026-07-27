import {
  mkdirSync,
  mkdtempSync,
  readFileSync,
  existsSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, describe, expect, it } from "vitest";
import { parse } from "yaml";

import {
  Artifact,
  addClaim,
  addExhibit,
  addExperiment,
  addResult,
  computeEvidenceInventory,
  createArtifact,
  defaultExhibitValidationMode,
  getExhibit,
  listExhibits,
  openSubmission,
  removeExhibit,
  validateStructure,
  writeSubmission,
} from "../src/index.js";

const tmpDirs: string[] = [];
function scratch(): string {
  const d = mkdtempSync(join(tmpdir(), "uas-exh-"));
  tmpDirs.push(d);
  return d;
}
afterAll(() => {
  for (const d of tmpDirs) rmSync(d, { recursive: true, force: true });
});

/** A minimal artifact with one experiment + claim so exhibit refs resolve. */
function baseArtifact(): Artifact {
  const a = createArtifact({ id: "art", title: "Bloom FPR" });
  addExperiment(a, {
    slug: "fpr-sweep",
    directory: "experiments/fpr_sweep",
    run: { command: "python run.py" },
  });
  addClaim(a, {
    id: "C4",
    statement: "FPR is U-shaped in k with a minimum near k*.",
    validators: [],
  });
  return a;
}

function findError(a: Artifact, re: RegExp): boolean {
  return validateStructure(a).errors.some((e) => re.test(`${e.path}: ${e.message}`));
}
function findWarning(a: Artifact, re: RegExp): boolean {
  return validateStructure(a).warnings.some((w) => re.test(`${w.path}: ${w.message}`));
}

describe("addExhibit builder (spec §2.3.1)", () => {
  it("adds, gets, lists and removes an exhibit", () => {
    const a = baseArtifact();
    addExhibit(a, {
      id: "X1",
      type: "figure",
      caption: "FPR vs k; U-shaped.",
      validates: ["C4"],
      path: "experiments/fpr_sweep/figure1.png",
    });
    expect(listExhibits(a).map((e) => e.id)).toEqual(["X1"]);
    expect(getExhibit(a, "X1")?.type).toBe("figure");
    expect(removeExhibit(a, "X1")).toBe(true);
    expect(listExhibits(a)).toEqual([]);
  });

  it("records a journal entry for the mutation", () => {
    const a = baseArtifact();
    addExhibit(
      a,
      { id: "X1", type: "figure", caption: "c", validates: ["C4"], path: "a/f.png" },
      { actor: "producer", rationale: "figure substantiates C4" },
    );
    const entry = a.journal.find((j) => j.target.kind === "exhibit");
    expect(entry?.target.id).toBe("X1");
    expect(entry?.op).toBe("add");
  });
});

describe("defaultExhibitValidationMode (spec §2.3.1)", () => {
  it("defaults a rendered exhibit to inspect and a proof to re-execute", () => {
    expect(defaultExhibitValidationMode("figure")).toBe("inspect");
    expect(defaultExhibitValidationMode("table")).toBe("inspect");
    expect(defaultExhibitValidationMode("listing")).toBe("inspect");
    expect(defaultExhibitValidationMode("proof")).toBe("re-execute");
  });
});

describe("exhibit serialization + round-trip (spec §5)", () => {
  it("writes exhibits.yml and indexes it in the manifest when exhibits exist", () => {
    const a = baseArtifact();
    const out = scratch();
    // stage the blob from a separate source tree so it is copied in (not warned as missing)
    const src = scratch();
    mkdirSync(join(src, "experiments/fpr_sweep"), { recursive: true });
    writeFileSync(join(src, "experiments/fpr_sweep/figure1.png"), "PNGDATA");
    addExhibit(a, {
      id: "X1",
      type: "figure",
      caption: "FPR vs k; U-shaped.",
      validates: ["C4"],
      path: "experiments/fpr_sweep/figure1.png",
      produced_by: "fpr-sweep",
      alt_text: "Line plot of FPR against k.",
      order: 1,
    });
    writeSubmission(a, out, { stageFrom: src });

    expect(existsSync(join(out, "exhibits.yml"))).toBe(true);
    expect(existsSync(join(out, "experiments/fpr_sweep/figure1.png"))).toBe(true);
    const doc = parse(readFileSync(join(out, "exhibits.yml"), "utf-8"));
    expect(doc.exhibits[0].id).toBe("X1");
    expect(doc.exhibits[0].caption).toBe("FPR vs k; U-shaped.");
    const manifest = parse(readFileSync(join(out, "manifest.yml"), "utf-8"));
    expect(manifest.paths.exhibits).toBe("exhibits.yml");
    expect(manifest.evidence_inventory.has_exhibits).toBe(true);
    expect(manifest.evidence_inventory.exhibit_count).toBe(1);

    const reopened = openSubmission(out);
    expect(reopened.exhibits).toHaveLength(1);
    expect(reopened.exhibits[0].alt_text).toBe("Line plot of FPR against k.");
  });

  it("omits exhibits.yml and its manifest index when no exhibits are declared (back-compat)", () => {
    const a = baseArtifact();
    const out = scratch();
    writeSubmission(a, out);
    expect(existsSync(join(out, "exhibits.yml"))).toBe(false);
    const manifest = parse(readFileSync(join(out, "manifest.yml"), "utf-8"));
    expect(manifest.paths.exhibits).toBeUndefined();
    expect(manifest.evidence_inventory.has_exhibits).toBe(false);
    expect(manifest.evidence_inventory.exhibit_count).toBe(0);
  });

  it("produces byte-identical output whether or not the exhibits API is touched", () => {
    const build = () => {
      const a = baseArtifact();
      const out = scratch();
      writeSubmission(a, out);
      return readFileSync(join(out, "manifest.yml"), "utf-8");
    };
    // a second artifact that adds then removes an exhibit must serialize identically
    const buildTouched = () => {
      const a = baseArtifact();
      addExhibit(a, { id: "X1", type: "figure", caption: "c", validates: ["C4"], path: "a/f.png" });
      removeExhibit(a, "X1");
      const out = scratch();
      writeSubmission(a, out);
      return readFileSync(join(out, "manifest.yml"), "utf-8");
    };
    expect(buildTouched()).toBe(build());
  });
});

describe("exhibit structural validation (spec §7)", () => {
  it("requires id, type, caption and path", () => {
    const a = baseArtifact();
    // @ts-expect-error intentionally missing required fields
    addExhibit(a, { id: "", type: "", caption: "  ", validates: ["C4"] });
    expect(findError(a, /exhibit requires `type`/)).toBe(true);
    expect(findError(a, /exhibit requires a non-empty `caption`/)).toBe(true);
    expect(findError(a, /exhibit requires `path`/)).toBe(true);
  });

  it("flags dangling claim, experiment and result references", () => {
    const a = baseArtifact();
    addExhibit(a, {
      id: "X1",
      type: "figure",
      caption: "c",
      validates: ["C_missing"],
      path: "a/f.png",
      produced_by: "no-such-exp",
      from_result: "R_missing",
    });
    expect(findError(a, /validates.*references unknown claim 'C_missing'/)).toBe(true);
    expect(findError(a, /produced_by.*references unknown experiment 'no-such-exp'/)).toBe(true);
    expect(findError(a, /from_result.*references unknown result 'R_missing'/)).toBe(true);
  });

  it("resolves a valid from_result cross-link without error", () => {
    const a = baseArtifact();
    addResult(a, { id: "R1", validates: ["C4"], evidence: "experiments/fpr_sweep/data.csv", kind: "metrics" });
    addExhibit(a, {
      id: "X1",
      type: "figure",
      caption: "c",
      validates: ["C4"],
      path: "a/f.png",
      from_result: "R1",
    });
    expect(findError(a, /exhibit\[X1\]/)).toBe(false);
  });

  it("rejects a path that collides with a generated file", () => {
    const a = baseArtifact();
    addExhibit(a, { id: "X1", type: "table", caption: "c", validates: ["C4"], path: "exhibits.yml" });
    expect(findError(a, /exhibit\[X1\]\.path.*collide with SDK-generated files/)).toBe(true);
  });

  it("accepts a statement-only proof exhibit (no rendered path)", () => {
    const a = baseArtifact();
    addExhibit(a, {
      id: "X1",
      type: "proof",
      caption: "Soundness of the FPR bound.",
      validates: ["C4"],
      statement: "For all k, FPR(k) >= (1 - e^{-kn/m})^k.",
    });
    expect(findError(a, /exhibit\[X1\]/)).toBe(false);
  });

  it("requires path or statement — a figure with neither is rejected", () => {
    const a = baseArtifact();
    // @ts-expect-error path intentionally omitted
    addExhibit(a, { id: "X1", type: "figure", caption: "c", validates: ["C4"] });
    expect(findError(a, /exhibit requires `path`/)).toBe(true);
  });

  it("rejects a pathless proof that also lacks a statement", () => {
    const a = baseArtifact();
    // @ts-expect-error path intentionally omitted
    addExhibit(a, { id: "X1", type: "proof", caption: "c", validates: ["C4"] });
    expect(findError(a, /exhibit requires `path`/)).toBe(true);
  });

  it("rejects an illegal validation_mode", () => {
    const a = baseArtifact();
    // @ts-expect-error illegal mode
    addExhibit(a, { id: "X1", type: "figure", caption: "c", validates: ["C4"], path: "a/f.png", validation_mode: "vibes" });
    expect(findError(a, /illegal validation_mode 'vibes'/)).toBe(true);
  });

  it("warns (not errors) on an unrecognized but non-empty type", () => {
    const a = baseArtifact();
    addExhibit(a, { id: "X1", type: "hologram", caption: "c", validates: ["C4"], path: "a/f.png" });
    expect(findWarning(a, /unrecognized exhibit type 'hologram'/)).toBe(true);
    expect(findError(a, /exhibit\[X1\]\.type/)).toBe(false);
  });

  it("detects a self-dependency and a dependency cycle in the proof DAG", () => {
    const self = baseArtifact();
    addExhibit(self, { id: "X1", type: "proof", caption: "c", validates: ["C4"], path: "p/x1.md", depends_on: ["X1"] });
    expect(findError(self, /exhibit cannot depend on itself/)).toBe(true);

    const cyclic = baseArtifact();
    addExhibit(cyclic, { id: "X1", type: "proof", caption: "c", validates: ["C4"], path: "p/x1.md", depends_on: ["X2"] });
    addExhibit(cyclic, { id: "X2", type: "proof", caption: "c", validates: ["C4"], path: "p/x2.md", depends_on: ["X1"] });
    expect(findError(cyclic, /exhibit dependency cycle/)).toBe(true);
  });

  it("accepts an acyclic proof -> lemma DAG", () => {
    const a = baseArtifact();
    addExhibit(a, { id: "X1", type: "proof", caption: "Theorem 2.", validates: ["C4"], path: "p/thm.md", statement: "E[FPR] >= (1/2)^k", depends_on: ["X2"] });
    addExhibit(a, { id: "X2", type: "proof", caption: "Lemma 1.", validates: ["C4"], path: "p/lemma.md", statement: "..." });
    expect(findError(a, /exhibit\[/)).toBe(false);
  });
});

describe("computeEvidenceInventory (spec §5.1)", () => {
  it("reports exhibit presence and count", () => {
    const a = baseArtifact();
    expect(computeEvidenceInventory(a).has_exhibits).toBe(false);
    addExhibit(a, { id: "X1", type: "figure", caption: "c", validates: ["C4"], path: "a/f.png" });
    const inv = computeEvidenceInventory(a);
    expect(inv.has_exhibits).toBe(true);
    expect(inv.exhibit_count).toBe(1);
  });
});
