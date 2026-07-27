/**
 * Structural validation (spec §7): the SDK's half of the validation split.
 *
 * The SDK checks that a submission is *well-formed* — required fields, legal enums, and
 * referential integrity. It does NOT check whether results actually support claims; that
 * semantic judgment stays with the evaluator. Hard problems (missing required field, dangling
 * reference, external dataset without a checksum, illegal enum, malformed validator) are
 * **errors** that block emission. "Incomplete but legal" situations (a claim with no
 * validator, a result whose evidence file is not yet present) are **warnings** — a partial
 * artifact is not malformed (spec §4.1).
 */

import {
  Artifact,
  CLAIM_STANCES,
  Claim,
  DISPOSITION_STATUSES,
  EXHIBIT_TYPES,
  pinnedDigest,
  Validator,
  VALIDATION_MODES,
} from "./model.js";

export interface Issue {
  path: string;
  message: string;
}

export interface ValidationReport {
  ok: boolean;
  errors: Issue[];
  warnings: Issue[];
}

export class StructuralError extends Error {
  readonly issues: Issue[];
  constructor(issues: Issue[]) {
    super(
      "structural validation failed:\n" +
        issues.map((i) => `  - ${i.path}: ${i.message}`).join("\n"),
    );
    this.name = "StructuralError";
    this.issues = issues;
  }
}

const GENERATED_RESERVED_PATHS = new Set([
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

function artifactRelativePathError(
  value: unknown,
  opts: { allowDirectory: boolean; reserveGenerated?: boolean; reserveGeneratedDescendants?: boolean },
): string | undefined {
  if (typeof value !== "string") return "must be a string";
  const trimmed = value.trim();
  if (!trimmed) return "must be non-empty";
  if (trimmed !== value) return "must not have leading or trailing whitespace";
  const slashPath = value.replace(/\\/g, "/");
  if (slashPath === "." || slashPath === "") return "must not point at the artifact root";
  if (slashPath.startsWith("/") || /^[A-Za-z]:/.test(slashPath)) return "must be relative to the artifact root";
  const parts = slashPath.split("/");
  if (parts.some((part) => part === ".." || part === ".")) return "must not contain . or .. path segments";
  if (!opts.allowDirectory && slashPath.endsWith("/")) return "must name a file, not a directory";
  const lowerSlashPath = slashPath.toLowerCase();
  const generatedCollision = [...GENERATED_RESERVED_PATHS].some((p) => {
    const lowerReserved = p.toLowerCase();
    return opts.reserveGenerated
      ? lowerSlashPath === lowerReserved || lowerSlashPath.startsWith(`${lowerReserved}/`)
      : opts.reserveGeneratedDescendants && lowerSlashPath.startsWith(`${lowerReserved}/`);
  });
  if (generatedCollision) return "must not collide with SDK-generated files";
  if (lowerSlashPath === ".sdk" || lowerSlashPath.startsWith(".sdk/")) return "must not be inside .sdk";
  return undefined;
}

function pushBlobPathError(errors: Issue[], path: string, value: unknown): void {
  const problem = artifactRelativePathError(value, { allowDirectory: true, reserveGenerated: true });
  if (problem) errors.push({ path, message: `referenced blob path ${problem}` });
}

function artifactPathKey(value: unknown): string | undefined {
  if (typeof value !== "string") return undefined;
  const trimmed = value.trim();
  if (!trimmed || trimmed !== value) return undefined;
  return trimmed.replace(/\\/g, "/").toLowerCase();
}

function collectAuthoredBlobRefs(a: Artifact): Array<{ path: string; value: string }> {
  const refs: Array<{ path: string; value: string }> = [];
  for (const d of a.datasets) {
    if (d.location?.kind === "in_artifact" && typeof d.location.path === "string") refs.push({ path: `dataset[${d.id}].location.path`, value: d.location.path });
    if (typeof d.sample?.path === "string") refs.push({ path: `dataset[${d.id}].sample.path`, value: d.sample.path });
  }
  for (const t of a.traces) if (typeof t.path === "string") refs.push({ path: `trace[${t.id}].path`, value: t.path });
  for (const r of a.results) if (typeof r.evidence === "string") refs.push({ path: `result[${r.id}].evidence`, value: r.evidence });
  for (const e of a.exhibits) {
    if (typeof e.path === "string") refs.push({ path: `exhibit[${e.id}].path`, value: e.path });
    if (typeof e.source === "string") refs.push({ path: `exhibit[${e.id}].source`, value: e.source });
  }
  if (a.paper) {
    if (typeof a.paper.pdf === "string") refs.push({ path: "paper.pdf", value: a.paper.pdf });
    if (typeof a.paper.source === "string") refs.push({ path: "paper.source", value: a.paper.source });
    if (typeof a.paper.claims_export === "string") refs.push({ path: "paper.claims_export", value: a.paper.claims_export });
    if (typeof a.paper.references_export === "string") refs.push({ path: "paper.references_export", value: a.paper.references_export });
  }
  if (typeof a.research_agent?.path === "string") refs.push({ path: "research_agent.path", value: a.research_agent.path });
  return refs;
}

function validatorIds(claim: Claim): Set<string> {
  const ids = new Set<string>();
  for (const v of claim.validators) if (v.id) ids.add(v.id);
  return ids;
}

/**
 * Detect cycles in the exhibit `depends_on` DAG (spec §2.3.1). Returns one representative path per
 * cycle found (e.g. `["X1", "X2", "X1"]`), so a proof→lemma graph can be asserted acyclic.
 */
function exhibitDependencyCycles(a: Artifact): string[][] {
  const adj = new Map<string, string[]>();
  for (const e of a.exhibits) adj.set(e.id, (e.depends_on ?? []).filter((d) => d !== e.id));
  const state = new Map<string, "visiting" | "done">();
  const cycles: string[][] = [];
  const seen = new Set<string>();
  const dfs = (node: string, stack: string[]): void => {
    state.set(node, "visiting");
    stack.push(node);
    for (const next of adj.get(node) ?? []) {
      if (!adj.has(next)) continue; // dangling ref already reported as an error
      if (state.get(next) === "visiting") {
        const cycle = [...stack.slice(stack.indexOf(next)), next];
        const key = [...cycle].sort().join("|");
        if (!seen.has(key)) {
          seen.add(key);
          cycles.push(cycle);
        }
      } else if (state.get(next) !== "done") {
        dfs(next, stack);
      }
    }
    stack.pop();
    state.set(node, "done");
  };
  for (const e of a.exhibits) if (!state.has(e.id)) dfs(e.id, []);
  return cycles;
}

function checkValidatorWellFormed(
  v: Validator,
  path: string,
  errors: Issue[],
): void {
  switch (v.kind) {
    case "builtin":
      if (!v.name)
        errors.push({ path, message: "builtin validator requires `name`" });
      break;
    case "procedure":
      if (!v.instructions)
        errors.push({
          path,
          message: "procedure validator requires `instructions`",
        });
      break;
    case "attest":
      if (!v.checks)
        errors.push({ path, message: "attest validator requires `checks`" });
      break;
    case "llm_judge":
      if (!v.criteria)
        errors.push({
          path,
          message: "llm_judge validator requires `criteria`",
        });
      break;
    default:
      errors.push({
        path,
        message: `unknown validator kind ${(v as { kind?: string }).kind ?? "<missing>"}`,
      });
  }
}

/** Validate an artifact's structure (spec §7). Pure — does not touch disk. */
export function validateStructure(a: Artifact): ValidationReport {
  const errors: Issue[] = [];
  const warnings: Issue[] = [];

  if (!a.id) errors.push({ path: "artifact.id", message: "`id` is required" });
  if (!a.title)
    errors.push({ path: "artifact.title", message: "`title` is required" });

  // environment: a run image SHOULD be pinned by digest (spec §4). A bare tag is mutable, so an
  // unpinned image is "incomplete but legal" — a WARNING (reproducibility risk), never an error.
  if (a.environment?.image) {
    const img = a.environment.image;
    if (!img.digest && !pinnedDigest(img.reference)) {
      warnings.push({
        path: `environment[${a.environment.name}].image`,
        message:
          "image is not pinned to a digest — `reference` is a mutable tag; " +
          "set `image.digest` (sha256:…) so the exact environment is reproducible",
      });
    }
  }

  // paper: a `paper` block MUST carry at least one non-empty of `pdf` / `source` (spec §2.6).
  // Both is fine; `source` alone (e.g. uncompiled LaTeX) is valid.
  if (a.paper) {
    const pdf = typeof a.paper.pdf === "string" ? a.paper.pdf.trim() : "";
    const source = typeof a.paper.source === "string" ? a.paper.source.trim() : "";
    if (!pdf && !source) {
      errors.push({
        path: "paper",
        message: "paper requires at least one of `pdf` or `source` (spec §2.6)",
      });
    }
    if (a.paper.pdf !== undefined) pushBlobPathError(errors, "paper.pdf", a.paper.pdf);
    if (a.paper.source !== undefined) pushBlobPathError(errors, "paper.source", a.paper.source);
    if (a.paper.claims_export !== undefined) pushBlobPathError(errors, "paper.claims_export", a.paper.claims_export);
    if (a.paper.references_export !== undefined) pushBlobPathError(errors, "paper.references_export", a.paper.references_export);
  }

  const experimentSlugs = new Set(a.experiments.map((e) => e.slug));
  const datasetIds = new Set(a.datasets.map((d) => d.id));
  const claimIds = new Set(a.claims.map((c) => c.id));
  const resultIds = new Set(a.results.map((r) => r.id));
  const exhibitIds = new Set(a.exhibits.map((e) => e.id));

  // datasets
  for (const d of a.datasets) {
    const p = `dataset[${d.id}]`;
    if (!d.id) errors.push({ path: p, message: "dataset requires `id`" });
    const loc = d.location;
    if (!loc || !loc.kind) {
      errors.push({ path: p, message: "dataset requires `location.kind`" });
      continue;
    }
    if (loc.kind === "in_artifact") pushBlobPathError(errors, `${p}.location.path`, loc.path);
    if (d.sample?.path !== undefined) pushBlobPathError(errors, `${p}.sample.path`, d.sample.path);
    if (loc.kind === "external" && !loc.sha256) {
      errors.push({
        path: `${p}.location`,
        message: "external dataset requires a `sha256` checksum",
      });
    }
    if (loc.kind === "in_container" && !loc.in_environment) {
      errors.push({
        path: `${p}.location`,
        message: "in_container dataset requires `in_environment`",
      });
    }
    if (loc.kind === "in_container" && !a.environment) {
      warnings.push({
        path: `${p}.location`,
        message: "in_container dataset but no environment declared",
      });
    }
  }

  // experiments
  for (const e of a.experiments) {
    const p = `experiment[${e.slug}]`;
    if (!e.slug)
      errors.push({ path: p, message: "experiment requires `slug`" });
    const directoryError = artifactRelativePathError(e.directory, { allowDirectory: true, reserveGenerated: true });
    if (!e.directory)
      errors.push({ path: p, message: "experiment requires `directory`" });
    else if (directoryError)
      errors.push({ path: `${p}.directory`, message: `experiment directory ${directoryError}` });
    if (!e.run || !e.run.command)
      errors.push({ path: p, message: "experiment requires `run.command`" });
    for (const u of e.uses_data ?? []) {
      if (!datasetIds.has(u.dataset))
        errors.push({
          path: `${p}.uses_data`,
          message: `references unknown dataset '${u.dataset}'`,
        });
    }
    for (const dep of e.depends_on ?? []) {
      if (!experimentSlugs.has(dep))
        errors.push({
          path: `${p}.depends_on`,
          message: `references unknown experiment '${dep}'`,
        });
    }
    if (e.runs_in && a.environment && e.runs_in !== a.environment.name) {
      errors.push({
        path: `${p}.runs_in`,
        message: `references unknown environment '${e.runs_in}'`,
      });
    }
    // disposition — lifecycle of an attempted experiment (spec §2.2.2)
    const disp = e.disposition;
    if (disp) {
      if (!DISPOSITION_STATUSES.includes(disp.status)) {
        errors.push({
          path: `${p}.disposition`,
          message: `illegal disposition status '${disp.status}'`,
        });
      }
      if (disp.status !== "active" && !(disp.rationale ?? "").trim()) {
        warnings.push({
          path: `${p}.disposition`,
          message: `${disp.status} experiment has no rationale — the process record is incomplete`,
        });
      }
      if (disp.superseded_by && !experimentSlugs.has(disp.superseded_by)) {
        errors.push({
          path: `${p}.disposition.superseded_by`,
          message: `references unknown experiment '${disp.superseded_by}'`,
        });
      }
      if (disp.status === "failed" && !disp.failure) {
        warnings.push({
          path: `${p}.disposition`,
          message: "failed experiment has no `failure` detail (stage/summary)",
        });
      }
    }
  }

  // traces
  for (const t of a.traces) {
    const p = `trace[${t.id}]`;
    if (!t.id) errors.push({ path: p, message: "trace requires `id`" });
    if (!t.path) errors.push({ path: p, message: "trace requires `path`" });
    else pushBlobPathError(errors, `${p}.path`, t.path);
    for (const slug of t.covers ?? []) {
      if (!experimentSlugs.has(slug))
        errors.push({
          path: `${p}.covers`,
          message: `references unknown experiment '${slug}'`,
        });
    }
  }

  // results
  for (const r of a.results) {
    const p = `result[${r.id}]`;
    if (!r.id) errors.push({ path: p, message: "result requires `id`" });
    if (!r.evidence)
      errors.push({ path: p, message: "result requires `evidence`" });
    else pushBlobPathError(errors, `${p}.evidence`, r.evidence);
    if (!r.kind) errors.push({ path: p, message: "result requires `kind`" });
    if (r.validation_mode && !VALIDATION_MODES.includes(r.validation_mode)) {
      errors.push({
        path: `${p}.validation_mode`,
        message: `illegal validation_mode '${r.validation_mode}'`,
      });
    }
    if (r.produced_by && !experimentSlugs.has(r.produced_by)) {
      errors.push({
        path: `${p}.produced_by`,
        message: `references unknown experiment '${r.produced_by}'`,
      });
    }
    for (const cid of r.validates ?? []) {
      if (!claimIds.has(cid))
        errors.push({
          path: `${p}.validates`,
          message: `references unknown claim '${cid}'`,
        });
    }
  }

  // exhibits (spec §2.3.1) — typed, captioned evidence linked to claims
  for (const e of a.exhibits) {
    const p = `exhibit[${e.id}]`;
    if (!e.id) errors.push({ path: p, message: "exhibit requires `id`" });
    if (!e.type) errors.push({ path: p, message: "exhibit requires `type`" });
    else if (!EXHIBIT_TYPES.includes(e.type)) {
      // Open/extensible enum: an unrecognized type is legal but flagged for review.
      warnings.push({
        path: `${p}.type`,
        message: `unrecognized exhibit type '${e.type}' (known: ${EXHIBIT_TYPES.join(" | ")})`,
      });
    }
    if (!e.caption || !e.caption.trim())
      errors.push({ path: p, message: "exhibit requires a non-empty `caption`" });
    // `path` is required, except a proof/derivation may substitute a formal `statement`
    // (a purely textual claim with no rendered file). Spec §2.3.1.
    const statementOnly =
      (e.type === "proof" || e.type === "derivation") && !!(e.statement && e.statement.trim());
    if (!e.path && !statementOnly)
      errors.push({
        path: p,
        message: "exhibit requires `path` (a proof/derivation may instead carry a `statement`)",
      });
    if (e.path) pushBlobPathError(errors, `${p}.path`, e.path);
    if (e.source !== undefined) pushBlobPathError(errors, `${p}.source`, e.source);
    if (e.validation_mode && !VALIDATION_MODES.includes(e.validation_mode)) {
      errors.push({
        path: `${p}.validation_mode`,
        message: `illegal validation_mode '${e.validation_mode}'`,
      });
    }
    if (e.produced_by && !experimentSlugs.has(e.produced_by)) {
      errors.push({
        path: `${p}.produced_by`,
        message: `references unknown experiment '${e.produced_by}'`,
      });
    }
    if (e.from_result && !resultIds.has(e.from_result)) {
      errors.push({
        path: `${p}.from_result`,
        message: `references unknown result '${e.from_result}'`,
      });
    }
    for (const cid of e.validates ?? []) {
      if (!claimIds.has(cid))
        errors.push({
          path: `${p}.validates`,
          message: `references unknown claim '${cid}'`,
        });
    }
    for (const dep of e.depends_on ?? []) {
      if (dep === e.id)
        errors.push({ path: `${p}.depends_on`, message: "exhibit cannot depend on itself" });
      else if (!exhibitIds.has(dep))
        errors.push({
          path: `${p}.depends_on`,
          message: `references unknown exhibit '${dep}'`,
        });
    }
  }
  for (const cycle of exhibitDependencyCycles(a)) {
    errors.push({
      path: `exhibit[${cycle[0]}].depends_on`,
      message: `exhibit dependency cycle: ${cycle.join(" -> ")}`,
    });
  }

  // claims + validators
  for (const c of a.claims) {
    const p = `claim[${c.id}]`;
    if (!c.id) errors.push({ path: p, message: "claim requires `id`" });
    if (!c.statement)
      errors.push({ path: p, message: "claim requires `statement`" });
    if (c.stance !== undefined && !CLAIM_STANCES.includes(c.stance)) {
      errors.push({
        path: `${p}.stance`,
        message: `invalid stance '${c.stance}' (expected ${CLAIM_STANCES.join(" | ")})`,
      });
    }
    for (const slug of c.tested_by ?? []) {
      if (!experimentSlugs.has(slug))
        errors.push({
          path: `${p}.tested_by`,
          message: `references unknown experiment '${slug}'`,
        });
    }
    if (c.validators.length === 0 && c.stance !== "hypothesis") {
      warnings.push({
        path: p,
        message: "claim has no validator — the evaluator will treat it as unverifiable",
      });
    }
    const localValidatorIds = validatorIds(c);
    for (let i = 0; i < c.validators.length; i++) {
      const v = c.validators[i];
      const vp = `${p}.validators[${v.id ?? i}]`;
      checkValidatorWellFormed(v, vp, errors);
      // gated_by must resolve to a validator id on the SAME claim (spec §7, resolved §11 Q13)
      const gatedBy = (v as { gated_by?: string }).gated_by;
      if (gatedBy) {
        if (!localValidatorIds.has(gatedBy)) {
          errors.push({
            path: `${vp}.gated_by`,
            message: `references unknown validator '${gatedBy}' on this claim`,
          });
        } else {
          const target = c.validators.find((x) => x.id === gatedBy);
          if (target && target.kind !== "attest") {
            errors.push({
              path: `${vp}.gated_by`,
              message: `gated_by must reference an attest validator, got '${target.kind}'`,
            });
          }
        }
      }
      // Result references must resolve. Field shape is kind-dependent (spec §3, audit A2):
      // a `builtin` validator uses singular `input:` (an object naming one Result); the other
      // kinds use plural `inputs:` (a list of Result ids). They are distinct fields, not typos.
      if (v.kind === "builtin") {
        const result = (v.input as { result?: string } | undefined)?.result;
        if (result && !resultIds.has(result))
          errors.push({
            path: `${vp}.input.result`,
            message: `references unknown result '${result}'`,
          });
      } else {
        for (const rid of v.inputs ?? []) {
          if (!resultIds.has(rid))
            errors.push({
              path: `${vp}.inputs`,
              message: `references unknown result '${rid}'`,
            });
        }
      }
    }
  }

  // assessments
  for (const s of a.assessments) {
    const p = `assessment[${s.id}]`;
    if (!s.id) errors.push({ path: p, message: "assessment requires `id`" });
    if (!s.dimension)
      errors.push({ path: p, message: "assessment requires `dimension`" });
    if (s.scope !== "artifact" && s.scope !== "paper")
      errors.push({
        path: `${p}.scope`,
        message: "scope must be 'artifact' or 'paper'",
      });
  }

  // research agent (spec §2.9) — optional; when present it MUST pin a `model` and declare at least
  // one `grounding_source`. Resolution of those sources against the shipped artifact is the evaluator's
  // job (it has disk access); the SDK only checks the element is well-formed.
  if (a.research_agent) {
    const ra = a.research_agent;
    const pathError = artifactRelativePathError(ra.path, { allowDirectory: false, reserveGenerated: true });
    if (pathError)
      errors.push({
        path: "research_agent.path",
        message: `research agent path ${pathError} (spec §2.9)`,
      });
    if (typeof ra.model !== "string" || !ra.model.trim())
      errors.push({
        path: "research_agent.model",
        message: "research agent requires a pinned `model` (spec §2.9)",
      });
    if (!Array.isArray(ra.grounding_sources) || ra.grounding_sources.length === 0) {
      errors.push({
        path: "research_agent.grounding_sources",
        message: "research agent requires at least one `grounding_source` (spec §2.9)",
      });
    } else {
      ra.grounding_sources.forEach((source, index) => {
        const sourceError = artifactRelativePathError(source, { allowDirectory: true, reserveGeneratedDescendants: true });
        if (sourceError) {
          errors.push({
            path: `research_agent.grounding_sources[${index}]`,
            message: `research agent grounding_source ${sourceError} (spec §2.9)`,
          });
        }
      });
    }
  }


  // Generated disposition markers and authored blobs must not overwrite each other.
  const authoredBlobRefs = collectAuthoredBlobRefs(a);
  const authoredBlobKeys = new Map<string, string>();
  for (const ref of authoredBlobRefs) {
    if (ref.value.endsWith("/") || ref.value.endsWith("\\")) continue;
    const key = artifactPathKey(ref.value);
    if (key) authoredBlobKeys.set(key, ref.path);
  }
  const dispositionMarkers = new Map<string, string>();
  for (const e of a.experiments) {
    if (!e.disposition || e.disposition.status === "active") continue;
    const dirKey = artifactPathKey(e.directory);
    if (!dirKey) continue;
    dispositionMarkers.set(`${dirKey}/disposition.md`, e.slug);
    const shadowedBlob = authoredBlobKeys.get(dirKey);
    if (shadowedBlob) {
      errors.push({
        path: `experiment[${e.slug}].directory`,
        message: `experiment directory collides with authored blob ${shadowedBlob}`,
      });
    }
  }
  for (const ref of authoredBlobRefs) {
    const key = artifactPathKey(ref.value);
    if (!key) continue;
    const markerSlug = dispositionMarkers.get(key);
    if (markerSlug) {
      errors.push({
        path: ref.path,
        message: `referenced blob path collides with generated disposition marker for experiment '${markerSlug}'`,
      });
    }
  }
  // journal — every recorded mutation should carry a rationale (spec §2.8, §4.2). A missing
  // rationale is "incomplete but legal" (the `warn` policy path), so it is a warning, not an error.
  for (const entry of a.journal) {
    if (!(entry.rationale ?? "").trim()) {
      warnings.push({
        path: `journal[#${entry.seq}]`,
        message: `mutation '${entry.op}' on ${entry.target.kind}[${entry.target.id}] has no rationale`,
      });
    }
  }

  return { ok: errors.length === 0, errors, warnings };
}
