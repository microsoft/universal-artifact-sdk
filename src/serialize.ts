/**
 * Serialization (spec §5): `writeSubmission` turns the in-memory model into the on-disk
 * `evaluable-artifact/v2` layout.
 *
 * The SDK serializes the **generated** index files (manifest, claims, results, datasets,
 * traces, journal, per-experiment DISPOSITION markers) plus reflection.md — all
 * reconstructable from the in-memory model — and computes integrity (SHA256SUMS,
 * .sdk/state.json). Blob files the producer places — the paper, evidence outputs, trace
 * records, in-artifact data, a research agent — are **authored**: the SDK copies them
 * verbatim (it cannot reconstruct them from the model) and never clobbers them. The
 * `.sdk/state.json` ledger classifies each file by this *nature*, independent of whether
 * `stageFrom` was passed on a given run (spec §5, §4.1). On re-emit the SDK rewrites the
 * generated files and leaves authored blobs untouched. An optional `stageFrom` root lets
 * the SDK copy referenced blobs into the submission for producers whose files live elsewhere.
 *
 * `writeSubmission` is idempotent: re-emitting an unchanged artifact rewrites the same bytes.
 */

import { createHash } from "node:crypto";
import {
  cpSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, posix, relative, sep } from "node:path";
import { stringify } from "yaml";

import { Artifact } from "./model.js";
import { computeEvidenceInventory } from "./inventory.js";
import { Issue, StructuralError, validateStructure } from "./validate.js";

const GENERATED_MARKER =
  "artifact-sdk/v1 (universal-artifact-sdk) — do not edit; regenerate";

export interface WriteOptions {
  /** Root to copy referenced blob files from (paper, evidence, traces, in-artifact data). */
  stageFrom?: string;
  /** If true, structural warnings do not appear in the report's `incomplete` flag. */
  quiet?: boolean;
}

export interface SubmissionReport {
  outDir: string;
  ok: boolean;
  incomplete: boolean;
  warnings: Issue[];
  filesWritten: string[];
  missingBlobs: string[];
}

function toPosix(p: string): string {
  return p.split(sep).join(posix.sep);
}

function sha256File(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function safeRelativePath(rel: string): string {
  const slashRel = rel.replace(/\\/g, posix.sep);
  const normalized = posix.normalize(slashRel);
  if (
    normalized === "." ||
    normalized === "" ||
    normalized === ".." ||
    normalized.startsWith(`..${posix.sep}`) ||
    posix.isAbsolute(normalized) ||
    /^[A-Za-z]:/.test(rel) ||
    slashRel.split(posix.sep).includes("..")
  ) {
    throw new Error(`Refusing to write outside submission root: ${rel}`);
  }
  return normalized;
}


function writeText(
  outDir: string,
  rel: string,
  content: string,
  written: string[],
): void {
  const safeRel = safeRelativePath(rel);
  const abs = join(outDir, safeRel);
  mkdirSync(dirname(abs), { recursive: true });
  writeFileSync(abs, content, { encoding: "utf-8" });
  written.push(toPosix(safeRel));
}

function yamlDoc(obj: unknown): string {
  return stringify(obj, { lineWidth: 0 });
}

/** Recursively list files under a dir, returning paths relative to `root` (posix). */
function walkFiles(root: string, dir = root, acc: string[] = []): string[] {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const abs = join(dir, entry.name);
    if (entry.isDirectory()) walkFiles(root, abs, acc);
    else acc.push(toPosix(relative(root, abs)));
  }
  return acc;
}

/** Collect blob paths the model references, so `stageFrom` can copy them in. */
const GENERATED_RESERVED_BLOBS = new Set([
  "manifest.yml",
  "claims.yml",
  "results.yml",
  "datasets.yml",
  "exhibits.yml",
  "traces.yml",
  "assessments.yml",
  "journal.yml",
  "reflection.md",
  "SHA256SUMS",
]);
const GENERATED_RESERVED_BLOB_KEYS = new Set([...GENERATED_RESERVED_BLOBS].map((p) => p.toLowerCase()));


function referencedBlobs(a: Artifact): string[] {
  const paths = new Set<string>();
  for (const d of a.datasets) {
    if (d.location.kind === "in_artifact") paths.add(d.location.path);
    if (d.sample?.path) paths.add(d.sample.path);
  }
  for (const r of a.results) if (r.evidence) paths.add(r.evidence);
  for (const e of a.exhibits) {
    if (e.path) paths.add(e.path);
    if (e.source) paths.add(e.source);
  }
  for (const t of a.traces) if (t.path) paths.add(t.path);
  if (a.paper) {
    if (a.paper.pdf) paths.add(a.paper.pdf);
    if (a.paper.source) paths.add(a.paper.source);
    if (a.paper.claims_export) paths.add(a.paper.claims_export);
    if (a.paper.references_export) paths.add(a.paper.references_export);
  }
  if (a.research_agent?.path) paths.add(a.research_agent.path);
  for (const source of a.research_agent?.grounding_sources ?? []) {
    if (!GENERATED_RESERVED_BLOB_KEYS.has(source.toLowerCase())) paths.add(source);
  }
  return [...paths];
}

function stageBlobs(
  a: Artifact,
  outDir: string,
  from: string,
  written: string[],
): string[] {
  const missing: string[] = [];
  for (const rel of referencedBlobs(a)) {
    const safeRel = safeRelativePath(rel);
    const src = join(from, safeRel);
    if (!existsSync(src)) {
      missing.push(safeRel);
      continue;
    }
    const dst = join(outDir, safeRel);
    mkdirSync(dirname(dst), { recursive: true });
    cpSync(src, dst, { recursive: true });
    if (statSync(dst).isDirectory()) {
      for (const f of walkFiles(dst)) written.push(toPosix(posix.join(safeRel, f)));
    } else {
      written.push(toPosix(safeRel));
    }
  }
  return missing;
}

/** Which referenced blobs are absent from the finished submission (→ incomplete warning). */
function findMissingBlobs(a: Artifact, outDir: string): string[] {
  return referencedBlobs(a).filter((rel) => !existsSync(join(outDir, safeRelativePath(rel))));
}

export function writeSubmission(
  a: Artifact,
  outDir: string,
  opts: WriteOptions = {},
): SubmissionReport {
  const report = validateStructure(a);
  if (!report.ok) throw new StructuralError(report.errors);

  mkdirSync(outDir, { recursive: true });
  // Two ledgers, split by *nature* of the file (not by whether it was touched
  // this run): `written` holds files the SDK serializes from the in-memory model
  // (regenerable, → generated_files); `staged` holds producer blobs copied in
  // verbatim (not reconstructable from the model, → authored_files, never clobbered).
  const written: string[] = [];
  const staged: string[] = [];

  // 0. stage producer blobs if a source root was given
  const stageMissing = opts.stageFrom ? stageBlobs(a, outDir, opts.stageFrom, staged) : [];

  // 1. reflection (authored, but the model may carry seed text)
  if (a.reflection !== undefined) {
    writeText(outDir, "reflection.md", a.reflection, written);
  }

  // 2. generated index files -------------------------------------------------
  const paths: Record<string, string> = {
    claims: "claims.yml",
    results: "results.yml",
    datasets: "datasets.yml",
  };
  if (a.traces.length > 0) paths.traces = "traces.yml";
  if (a.exhibits.length > 0) paths.exhibits = "exhibits.yml";
  if (a.assessments.length > 0) paths.assessments = "assessments.yml";
  if (a.journal.length > 0) paths.journal = "journal.yml";

  const manifest = {
    _generated: GENERATED_MARKER,
    format_version: a.format_version,
    sdk_version: a.sdk_version,
    id: a.id,
    title: a.title,
    ...(a.producer ? { producer: a.producer } : {}),
    ...(a.environment ? { environment: a.environment } : {}),
    experiments: a.experiments,
    paths,
    ...(a.paper ? { paper: a.paper } : {}),
    ...(a.research_agent ? { research_agent: a.research_agent } : {}),
    evidence_inventory: computeEvidenceInventory(a),
  };
  writeText(outDir, "manifest.yml", yamlDoc(manifest), written);

  writeText(
    outDir,
    "claims.yml",
    yamlDoc({ _generated: GENERATED_MARKER, claims: a.claims }),
    written,
  );
  writeText(
    outDir,
    "results.yml",
    yamlDoc({ _generated: GENERATED_MARKER, results: a.results }),
    written,
  );
  writeText(
    outDir,
    "datasets.yml",
    yamlDoc({ _generated: GENERATED_MARKER, datasets: a.datasets }),
    written,
  );
  if (a.exhibits.length > 0) {
    writeText(
      outDir,
      "exhibits.yml",
      yamlDoc({ _generated: GENERATED_MARKER, exhibits: a.exhibits }),
      written,
    );
  }
  if (a.traces.length > 0) {
    writeText(
      outDir,
      "traces.yml",
      yamlDoc({ _generated: GENERATED_MARKER, traces: a.traces }),
      written,
    );
  }
  if (a.assessments.length > 0) {
    writeText(
      outDir,
      "assessments.yml",
      yamlDoc({ _generated: GENERATED_MARKER, assessments: a.assessments }),
      written,
    );
  }
  if (a.journal.length > 0) {
    writeText(
      outDir,
      "journal.yml",
      yamlDoc({ _generated: GENERATED_MARKER, journal: a.journal }),
      written,
    );
  }

  // 2b. per-experiment disposition markers for non-active (attempted/dropped) experiments,
  //     so a reviewer browsing the tree sees what was tried and why (spec §2.2.2).
  for (const e of a.experiments) {
    const disp = e.disposition;
    if (!disp || disp.status === "active") continue;
    const lines = [
      `> **Auto-generated** by ${GENERATED_MARKER}`,
      "",
      `# Experiment \`${e.slug}\` — ${disp.status}`,
      "",
      `**Status:** ${disp.status}`,
      ...(disp.superseded_by
        ? [`**Superseded by:** \`${disp.superseded_by}\``]
        : []),
      ...(disp.failure
        ? [`**Failure:** ${disp.failure.stage} — ${disp.failure.summary}`]
        : []),
      "",
      "## Rationale",
      "",
      disp.rationale || "_(no rationale recorded)_",
      "",
    ];
    writeText(
      outDir,
      posix.join(e.directory, "DISPOSITION.md"),
      lines.join("\n"),
      written,
    );
  }

  // 3. integrity: SHA256SUMS over every shipped file, then .sdk/state.json ----
  const generatedIndex = new Set(written.map((w) => w));
  const allFiles = walkFiles(outDir)
    .filter((f) => f !== "SHA256SUMS" && !f.startsWith(".sdk/"))
    .sort();
  const sums = allFiles
    .map((rel) => `${sha256File(join(outDir, rel))}  ${rel}`)
    .join("\n");
  writeText(outDir, "SHA256SUMS", sums + "\n", written);

  const authored: Record<string, string> = {};
  for (const rel of allFiles) {
    if (!generatedIndex.has(rel)) authored[rel] = sha256File(join(outDir, rel));
  }
  const state = {
    _generated: GENERATED_MARKER,
    sdk_version: a.sdk_version,
    generated_files: [...generatedIndex].sort(),
    authored_files: authored,
  };
  writeText(
    outDir,
    ".sdk/state.json",
    JSON.stringify(state, null, 2) + "\n",
    written,
  );

  const missingBlobs = [...new Set([...stageMissing, ...findMissingBlobs(a, outDir)])].sort();
  const warnings: Issue[] = [
    ...report.warnings,
    ...missingBlobs.map((rel) => ({
      path: `blob[${rel}]`,
      message: "referenced file not present in submission (incomplete)",
    })),
  ];

  return {
    outDir,
    ok: true,
    incomplete: !opts.quiet && warnings.length > 0,
    warnings,
    filesWritten: [...new Set([...written, ...staged])].sort(),
    missingBlobs,
  };
}
