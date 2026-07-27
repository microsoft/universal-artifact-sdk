/**
 * Object model for the Universal Artifact SDK (artifact-sdk/v1).
 *
 * These types are the in-memory shape a producer builds; `writeSubmission` serializes
 * them into the on-disk `evaluable-artifact/v2` format. Field names track
 * SPEC.md §2–§3 (provisional until schema generation, §11 Q1).
 *
 * The model is vendor-neutral: nothing producer-specific lives here (spec §9).
 */

export const SDK_VERSION = "artifact-sdk/v1";
export const FORMAT_VERSION = "evaluable-artifact/v2";

/** How a claim is validated from evidence (spec §3.1). */
export type ValidationMode = "re-execute" | "re-analyze" | "inspect" | "attest";

export const VALIDATION_MODES: readonly ValidationMode[] = [
  "re-execute",
  "re-analyze",
  "inspect",
  "attest",
];

/** Evidence kind carried by a Result (spec §2.3, expanded). Open/extensible. */
export type ResultKind =
  | "metrics"
  | "figure"
  | "table"
  | "log"
  | "proof"
  | "artifact"
  | "transcript"
  | "survey"
  | "codebook"
  | "argument"
  | "external_reference"
  | (string & {});

/** Names in the builtin validator catalog shipped in v1 (spec §3.2, resolved §11 Q2). */
export type BuiltinCheck =
  | "numeric_close"
  | "numeric_threshold"
  | "monotonic"
  | "exact_match"
  | "contains"
  | "output_present";

// --- validators (spec §3) ---------------------------------------------------

export interface BuiltinValidator {
  id?: string;
  kind: "builtin";
  name: BuiltinCheck | (string & {});
  input?: Record<string, unknown>;
  params?: Record<string, unknown>;
  gated_by?: string;
}

export interface ProcedureValidator {
  id?: string;
  kind: "procedure";
  instructions: string;
  tools?: Array<{ name: string; version?: string }>;
  inputs?: string[];
  success_criteria?: string;
  timeout?: string;
  gated_by?: string;
}

/** Provenance / integrity / ethics attestation — gates inspect, never verdicts (spec §3.5). */
export interface AttestValidator {
  id?: string;
  kind: "attest";
  checks:
    "provenance" | "integrity" | "ethics" | "citations_exist" | (string & {});
  inputs?: string[];
}

/** Advisory NL rubric — the `inspect` mode (spec §3.4). */
export interface LlmJudgeValidator {
  id?: string;
  kind: "llm_judge";
  criteria: string;
  inputs?: string[];
  gated_by?: string;
}

export type Validator =
  BuiltinValidator | ProcedureValidator | AttestValidator | LlmJudgeValidator;

// --- graph nodes (spec §2) --------------------------------------------------

export interface Environment {
  name: string;
  image: { reference: string; digest?: string };
  os?: string;
  hardware?: { cpu?: string; gpu?: string; min_ram_gb?: number };
}

/**
 * Extract the immutable `sha256:…` digest embedded in a pinned image reference
 * (`repo[:tag]@sha256:<64-hex>`), or `undefined` when the reference is a bare, mutable tag.
 * Pure/offline — the SDK never contacts a registry. A pinned reference is what makes the run
 * environment reproducible (spec §4); the builder uses this to auto-fill `image.digest`.
 */
export function pinnedDigest(reference: string | undefined): string | undefined {
  const m = /@(sha256:[a-f0-9]{64})$/i.exec(reference ?? "");
  return m ? m[1].toLowerCase() : undefined;
}

export type DatasetLocation =
  | { kind: "in_artifact"; path: string }
  | { kind: "in_container"; path: string; in_environment: string }
  | {
      kind: "external";
      uri: string;
      sha256: string;
      bytes?: number;
      access?: "public" | "requires_credentials" | "license_gated";
      license?: string;
    };

/** Human-subjects / study provenance (spec §2.7, resolved §11 Q14). All advisory. */
export interface StudyMetadata {
  ethics_approval?: string;
  consent_basis?: string;
  deidentification?: string;
  redaction_note?: string;
  sampling?: string;
  extra?: Record<string, unknown>;
}

export interface Dataset {
  id: string;
  description?: string;
  location: DatasetLocation;
  prepare?: string;
  sample?: { path: string; sha256?: string };
  study?: StudyMetadata;
}

export interface RunSpec {
  command: string;
  entrypoint?: string;
  working_dir?: string;
  args?: string[];
  env?: Record<string, string>;
  seed?: number;
}

export interface Experiment {
  slug: string;
  directory: string;
  run: RunSpec;
  uses_data?: Array<{ dataset: string; at: string }>;
  depends_on?: string[];
  expected_runtime?: string;
  runs_in?: string;
  /** Research-process lifecycle (spec §2.2.2). Absent ⇒ `active` (back-compatible). */
  disposition?: Disposition;
}

/** Lifecycle status of a retained experiment (spec §2.2.2). */
export type DispositionStatus =
  "active" | "superseded" | "abandoned" | "failed";

export const DISPOSITION_STATUSES: readonly DispositionStatus[] = [
  "active",
  "superseded",
  "abandoned",
  "failed",
];

/**
 * Why an attempted experiment is not in the reported (active) set (spec §2.2.2). Retaining these
 * — rather than deleting them — preserves the research process: what was tried, and why it was
 * dropped. `rationale` is required for any non-`active` status.
 */
export interface Disposition {
  status: DispositionStatus;
  rationale: string;
  /** slug of the replacement, when `status === "superseded"`. */
  superseded_by?: string;
  /** where/why it broke, when `status === "failed"`. */
  failure?: { stage: string; summary: string };
}

/** The record of what actually ran (spec §2.2.1). Envelope only; body opaque (§11 Q12). */
export interface Trace {
  id: string;
  kind:
    | "agent_session"
    | "execution_log"
    | "build_log"
    | "notebook"
    // A human-in-the-loop interaction log (reviewer clarifications + stage-gate decisions), NOT a
    // record of a run. Evaluators MUST exclude it from run-oriented dimensions (execution authenticity,
    // trace-report faithfulness); it carries no `terminal_state`. See spec §2.2.1.
    | "human_interaction"
    | "other"
    | (string & {});
  path: string;
  covers?: string[];
  terminal_state?:
    | "completed_with_outputs"
    | "planning_only"
    | "debugging_no_run"
    | "aborted"
    | "unknown";
  counters?: Record<string, number>;
}

/** Named cell-level handle into evidence, used by numeric validators (spec §2.3). */
export type Locator = Record<string, unknown>;

/** Qualitative support, in lieu of numeric locators (spec §2.3). */
export interface QualitativeSupport {
  excerpts?: Array<{ file: string; lines?: string }>;
  codebook?: string;
  inter_rater_reliability?: { metric: string; value: number };
}

export interface Result {
  id: string;
  produced_by?: string;
  validates: string[];
  evidence: string;
  kind: ResultKind;
  validation_mode?: ValidationMode;
  locators?: Record<string, Locator>;
  support?: QualitativeSupport;
  supersedes?: string;
}

/**
 * Genre of a typed exhibit (spec §2.3.1). Open/extensible: an unrecognized type is carried
 * verbatim, not rejected.
 */
export type ExhibitType =
  | "figure"
  | "table"
  | "proof"
  | "derivation"
  | "listing"
  | (string & {});

export const EXHIBIT_TYPES: readonly ExhibitType[] = [
  "figure",
  "table",
  "proof",
  "derivation",
  "listing",
];

/**
 * A typed, captioned evidence artifact that substantiates one or more claims (spec §2.3.1).
 *
 * An Exhibit is the *human-consumable rendering* that stands behind a claim — a figure, table,
 * proof, derivation, or code listing — as distinct from a {@link Result} (a computed
 * outcome/measurement). They are siblings, cross-linkable via `from_result`, not subclasses:
 * an exhibit carries presentation concerns (a self-contained `caption`, an optional `alt_text`)
 * that a result does not. All exhibit types share the spine — `caption`, `validates`,
 * `produced_by`, `validation_mode` — and add additive, type-specific fields.
 *
 * The whole collection is optional and evidence-conditioned: a submission that declares no
 * exhibits is not malformed, and consumers keep their heuristic exhibit→claim inference as a
 * fallback (spec §2.3.1).
 */
export interface Exhibit {
  id: string;
  type: ExhibitType;
  /** Self-contained caption. A reader should understand the exhibit from this alone. REQUIRED. */
  caption: string;
  /** Claim id(s) this exhibit substantiates; many-to-many, mirrors {@link Result.validates}. */
  validates: string[];
  /** Primary/rendered form of the exhibit (safe relative path). */
  path: string;
  /** Experiment slug that produced the exhibit (optional provenance). */
  produced_by?: string;
  /** How a reviewer confirms the exhibit. Absent ⇒ inferred from `type` (spec §3.1). */
  validation_mode?: ValidationMode;
  /** Vector/source companion for a rendered figure (e.g. the PDF behind a PNG). */
  source?: string;
  /** Accessibility description for a figure/table. */
  alt_text?: string;
  /** Display order within a claim. */
  order?: number;
  /** Cross-link to the {@link Result} this exhibit renders. */
  from_result?: string;
  /** Formal statement, for a `proof`/`derivation`. */
  statement?: string;
  /** Exhibit id(s) this one depends on (e.g. a proof → its lemmas). Must be acyclic. */
  depends_on?: string[];
  /** Source language, for a `listing`. */
  language?: string;
}

/**
 * Author-declared epistemic standing of a claim (spec §2.4.1).
 *
 * - `finding` — the author asserts this is demonstrated by the artifact's
 *   evidence. This is the default, and the bar the evaluator holds it to is
 *   substantiation ("does the evidence support it?").
 * - `hypothesis` — a proposed statement the author set out to test. It may
 *   carry no passing validator yet. A hypothesis whose testing experiment ends
 *   up `abandoned`/`failed` (§2.2.2) is a preserved **negative result**, assessed
 *   on whether it was honestly tested and reported — not on whether it holds.
 */
export type ClaimStance = "hypothesis" | "finding";
export const CLAIM_STANCES: readonly ClaimStance[] = ["hypothesis", "finding"];

/** The default stance for a claim that does not declare one (spec §2.4.1). */
export const DEFAULT_CLAIM_STANCE: ClaimStance = "finding";

export interface Claim {
  id: string;
  statement: string;
  /**
   * Author-declared standing (spec §2.4.1). Absent ⇒ `finding` (back-compat):
   * a plain `addClaim` keeps asserting a demonstrated result.
   */
  stance?: ClaimStance;
  /**
   * Slugs of the experiment(s) that test this claim (spec §2.4.1). Links a
   * `hypothesis` to the disposition of the experiment that resolves it, so a
   * refuted hypothesis reads as a negative result rather than a dangling claim.
   */
  tested_by?: string[];
  paper_ref?: { section?: string; figure?: string; page?: number | string };
  validators: Validator[];
}

/** Whole-submission evaluation dimension (spec §2.1.1). Mostly evaluator-written. */
export interface Assessment {
  id: string;
  dimension:
    | "execution_authenticity"
    | "trace_report_faithfulness"
    | "citation_integrity"
    | "limitation_transparency"
    | (string & {});
  scope: "artifact" | "paper";
  evidence?: string[];
  validator?: Validator;
}

export interface Paper {
  /** Compiled paper. At least one of `pdf` / `source` MUST be present (spec §2.6). */
  pdf?: string;
  /** LaTeX/Markdown source — a single file or a directory (multi-file projects staged verbatim). */
  source?: string;
  claims_export?: string;
  references_export?: string;
}

// --- research agent (spec §2.9) ---------------------------------------------

/**
 * Optional producer-shipped Q&A witness (spec §2.9). An evidence-grounded agent that answers
 * questions about *this* submission's research, methods, data, results — and its dead ends. It is
 * an **additional evidence source the evaluator audits**, never an authority: an advocate for its own
 * work, so advisory and lowest-trust. Optional/absence-tolerant. The `path` names the authored
 * persona/guide file (`research-agent.md`, staged as a blob); the structured fields below are the
 * machine-readable, evaluator-consumed contract mirrored into the manifest.
 */
export interface ResearchAgent {
  /** Relative path to the authored persona/guide markdown (default `research-agent.md`). */
  path: string;
  /** Pinned, concrete model reference (e.g. `copilot/gpt-5.5@2026-06-01`) — reproducibility. */
  model: string;
  /** Artifact files/dirs the agent is authoritative over; the evaluator resolves these against disk. */
  grounding_sources: string[];
  /** Declared capability areas (open vocab), e.g. `research`, `results`, `negative-results`. */
  scope?: string[];
}

// --- provenance journal (spec §2.8) -----------------------------------------

/** The mutation a journal entry records (spec §2.8). */
export type JournalOp =
  "add" | "replace" | "remove" | "abandon" | "attach" | "set";

/** The element a journal entry is about (spec §2.8). */
export interface JournalTarget {
  kind:
    | "experiment"
    | "result"
    | "claim"
    | "exhibit"
    | "dataset"
    | "trace"
    | "assessment"
    | "environment"
    | "paper"
    | "reflection"
    | "research_agent"
    | (string & {});
  id: string;
}

/**
 * One append-only entry in the artifact's edit history (spec §2.8). Every mutation through the
 * authoring API records what changed and — crucially — *why*, so a reviewer can read the
 * narrated process, not just the final state.
 */
export interface JournalEntry {
  seq: number;
  timestamp: string; // ISO-8601
  actor: string; // e.g. "agent:experiment-agent" | "human:reviewer"
  op: JournalOp;
  target: JournalTarget;
  rationale: string;
  before?: unknown;
  after?: unknown;
}

/** How aggressively the SDK insists on a rationale for each mutation (spec §4.2). */
export type RationalePolicy = "required" | "prompt" | "warn";

/**
 * Per-session journaling configuration (spec §4.2). Transient: it drives the authoring API but
 * is NOT part of the serialized artifact. Set via `configureJournal`.
 */
export interface JournalConfig {
  /** `warn` (default), `prompt` (call `onMissingRationale`), or `required` (throw). */
  policy: RationalePolicy;
  /** Default actor stamped on entries when a `ChangeContext` omits one. */
  actor: string;
  /** Under `policy: "prompt"`, asked to supply a rationale when a mutation omits one. */
  onMissingRationale?: (change: PendingChange) => string;
  /** Injectable clock (testing); defaults to `() => new Date().toISOString()`. */
  now?: () => string;
}

/** The change handed to `onMissingRationale` before it commits (spec §4.2). */
export interface PendingChange {
  op: JournalOp;
  target: JournalTarget;
}

// --- root -------------------------------------------------------------------

export interface Artifact {
  format_version: string;
  sdk_version: string;
  id: string;
  title: string;
  producer?: Record<string, unknown>;
  environment?: Environment;
  datasets: Dataset[];
  experiments: Experiment[];
  traces: Trace[];
  results: Result[];
  claims: Claim[];
  /** Typed, captioned evidence artifacts linked to claims (spec §2.3.1). Serialized to `exhibits.yml`. */
  exhibits: Exhibit[];
  assessments: Assessment[];
  paper?: Paper;
  /** Optional producer Q&A witness (spec §2.9); serialized to `manifest.research_agent`. */
  research_agent?: ResearchAgent;
  reflection?: string;
  /** Append-only edit history (spec §2.8). Serialized to `journal.yml`. */
  journal: JournalEntry[];
  /** Transient journaling config (spec §4.2); never serialized. */
  journalConfig?: JournalConfig;
}

/** Default validation_mode inferred from a Result's `kind` (spec §2.3). */
export function defaultValidationMode(kind: ResultKind): ValidationMode {
  switch (kind) {
    case "metrics":
    case "table":
    case "figure":
      return "re-analyze";
    case "proof":
    case "log":
      return "re-execute";
    case "external_reference":
      return "attest";
    default:
      return "inspect";
  }
}

/**
 * Default `validation_mode` inferred from an Exhibit's `type` (spec §2.3.1). An exhibit is a
 * human-consumable rendering, so it defaults to `inspect` (a reviewer reads it and judges support);
 * a machine-checkable `proof` defaults to `re-execute` (run the checker). This differs from
 * {@link defaultValidationMode} for Results, where a `figure` renders a re-analyzable measurement.
 */
export function defaultExhibitValidationMode(type: ExhibitType): ValidationMode {
  switch (type) {
    case "proof":
      return "re-execute";
    default:
      return "inspect";
  }
}
