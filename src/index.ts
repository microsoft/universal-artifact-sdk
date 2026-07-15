/**
 * Universal Artifact SDK — TypeScript binding (artifact-sdk/v1).
 *
 * Authoring API that emits the `evaluable-artifact/v2` submission format an evaluator consumes.
 * See SPEC.md.
 *
 * Quickstart:
 * ```ts
 * import { createArtifact, addExperiment, addResult, addClaim, writeSubmission } from "@microsoft/universal-artifact-sdk";
 * const a = createArtifact({ id: "expt-42", title: "…" });
 * // add environment / datasets / experiments / results / claims …
 * writeSubmission(a, "./out");
 * ```
 */

export * from "./model.js";
export * from "./builder.js";
export * from "./validate.js";
export * from "./inventory.js";
export * from "./serialize.js";
export * from "./open.js";
