/**
 * Contribution-specific schema, bibliography resolution and conservative file ownership.
 * Existing indexes keep their legacy behavior; this boundary must never lose authored edits.
 */
import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync, statSync } from "node:fs";
import { isAbsolute, join, resolve } from "node:path";
import { Ajv } from "ajv";
import { parse } from "yaml";
import type { Artifact } from "../model.js";

const schema = JSON.parse(readFileSync(
  new URL("../../schema/evaluable-artifact-v3.schema.json", import.meta.url), "utf-8",
));
const check = new Ajv({ allErrors: true, strict: false }).compile({
  $defs: schema.$defs,
  ...schema.properties.contributions,
});

export function contributionShapeIssues(value: unknown): Array<{ path: string; message: string }> {
  const records: Array<Record<string, unknown> | null> = Array.isArray(value) ? value : [];
  if (check(value)) return [];
  return (check.errors ?? []).map((error) => {
    const parts = error.instancePath.split("/").slice(1)
      .map((p) => p.replace(/~1/g, "/").replace(/~0/g, "~"));
    const first = parts.shift();
    const record = first === undefined ? undefined : records[Number(first)];
    const id = typeof record?.id === "string" ? record.id : first;
    let path = first === undefined ? "contributions" : `contribution[${id}]`;
    for (const p of parts) path += /^\d+$/.test(p) ? `[${p}]` : `.${p}`;
    if (error.keyword === "required") path += `.${error.params.missingProperty}`;
    return { path, message: error.message ?? "invalid contribution declaration" };
  });
}

export function safeContributionPath(root: string, rel: unknown): string {
  if (typeof rel !== "string" || !rel || rel.trim() !== rel) {
    throw new Error("invalid contributions index path");
  }
  const slash = rel.replace(/\\/g, "/");
  const parts = slash.split("/");
  const reserved = new Set([
    "manifest.yml", "claims.yml", "results.yml", "datasets.yml", "exhibits.yml",
    "traces.yml", "assessments.yml", "journal.yml", "reflection.md", "sha256sums", ".sdk",
  ]);
  if (
    isAbsolute(slash) || /^[A-Za-z]:/.test(slash) ||
    parts.some((p) => !p || p === "." || p === "..") ||
    reserved.has(parts[0].toLowerCase())
  ) {
    throw new Error(`unsafe contributions index path: ${rel}`);
  }
  let path = resolve(root);
  for (const part of parts) {
    path = join(path, part);
    try {
      if (lstatSync(path).isSymbolicLink()) throw new Error(`symlink in contributions index path: ${rel}`);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") throw error;
    }
  }
  return path;
}

export function contributionHash(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

const sources = new WeakMap<Artifact, { path: string; hash: string }>();

export function captureContributionSource(a: Artifact, path: string): void {
  sources.set(a, { path: resolve(path), hash: contributionHash(path) });
}

/** Preflight before any output changes; removal is allowed only with matching ownership hash. */
export function contributionWritePlan(a: Artifact, root: string): { path: string; remove: boolean } {
  const path = safeContributionPath(root, "contributions.yml");
  if (!existsSync(path)) return { path, remove: false };
  const hash = contributionHash(path);
  const statePath = join(root, ".sdk/state.json");
  let state: { generated_hashes?: Record<string, string> } = {};
  if (existsSync(statePath)) {
    try {
      state = JSON.parse(readFileSync(statePath, "utf-8")) ?? {};
    } catch {
      // Untrusted ownership is not ownership.
    }
  }
  const owned = state.generated_hashes?.["contributions.yml"] === hash;
  const source = sources.get(a);
  if (
    (a.contributions?.length ?? 0) > 0 && !owned &&
    !(source?.path === resolve(path) && source.hash === hash)
  ) {
    throw new Error("Refusing to overwrite authored or externally edited contributions.yml; reopen before editing");
  }
  return { path, remove: (a.contributions?.length ?? 0) === 0 && owned };
}

/** Existing references_export IDs (id/key/citation-key or BibTeX entry keys), never inferred novelty. */
export function referenceIdsFromText(text: string, bibtex: boolean): string[] | undefined {
  if (bibtex) {
    const ids: string[] = [];
    const entries = /@\s*([A-Za-z]+)\s*([{(])/g;
    const input = text.replace(/^%.*$/gm, "");
    let match: RegExpExecArray | null;
    while ((match = entries.exec(input))) {
      const start = entries.lastIndex;
      const end = match[2] === "{" ? "}" : ")";
      let depth = 1;
      let braces = 0;
      let quoted = false;
      let cursor = start;
      for (; cursor < input.length; cursor++) {
        const ch = input[cursor];
        if (ch === "\\") { cursor++; continue; }
        if (ch === '"' && (match[2] === "(" ? braces === 0 : depth === 1)) quoted = !quoted;
        if (quoted) continue;
        if (match[2] === "(") {
          if (ch === "{") braces++;
          if (ch === "}") braces--;
          if (braces > 0 || ch === "}") continue;
        }
        if (ch === match[2]) depth++;
        if (ch === end) depth--;
        if (depth === 0) break;
      }
      if (depth !== 0) return undefined;
      entries.lastIndex = cursor + 1;
      if (["comment", "string", "preamble"].includes(match[1].toLowerCase())) continue;
      const key = /^\s*([^,\s]+)\s*,/.exec(input.slice(start, cursor))?.[1];
      if (!key) return undefined;
      ids.push(key);
    }
    return ids.length || !text.trim() ? ids : undefined;
  }
  try {
    const data = parse(text);
    const refs = Array.isArray(data) ? data : data?.references;
    if (!Array.isArray(refs)) return undefined;
    const ids = refs.map((r) => r?.id ?? r?.key ?? r?.["citation-key"]);
    return ids.every((id) => typeof id === "string") ? ids : undefined;
  } catch { return undefined; }
}

export function resolveReferenceIds(a: Artifact, roots: string[]): string[] | undefined {
  const rel = a.paper?.references_export;
  if (!rel) return undefined;
  // validateStructure checks this blob path before this helper is called.
  for (const root of roots) {
    const path = join(root, rel);
    try {
      if (existsSync(path) && statSync(path).isFile()) {
        return referenceIdsFromText(readFileSync(path, "utf-8"), /\.bib$/i.test(rel));
      }
    } catch { return undefined; }
  }
  return undefined;
}
