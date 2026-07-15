/**
 * openSubmission (spec §4, §4.1): reopen an existing on-disk submission back into the model so
 * the next change is a small edit, not a from-scratch rebuild. Reads the generated index files;
 * authored blobs stay on disk untouched and are preserved on the next `writeSubmission`.
 */

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { parse } from "yaml";

import { Artifact, FORMAT_VERSION, SDK_VERSION } from "./model.js";

function readYaml(path: string): Record<string, unknown> {
  return (parse(readFileSync(path, "utf-8")) as Record<string, unknown>) ?? {};
}

export function openSubmission(dir: string): Artifact {
  const manifestPath = join(dir, "manifest.yml");
  if (!existsSync(manifestPath)) {
    throw new Error(`openSubmission: no manifest.yml in ${dir}`);
  }
  const manifest = readYaml(manifestPath);
  const paths = (manifest.paths as Record<string, string>) ?? {};

  const readList = <T>(rel: string | undefined, key: string): T[] => {
    if (!rel) return [];
    const p = join(dir, rel);
    if (!existsSync(p)) return [];
    return ((readYaml(p)[key] as T[]) ?? []) as T[];
  };

  const a: Artifact = {
    format_version: (manifest.format_version as string) ?? FORMAT_VERSION,
    sdk_version: (manifest.sdk_version as string) ?? SDK_VERSION,
    id: (manifest.id as string) ?? "",
    title: (manifest.title as string) ?? "",
    producer: manifest.producer as Record<string, unknown> | undefined,
    environment: manifest.environment as Artifact["environment"],
    datasets: readList(paths.datasets ?? "datasets.yml", "datasets"),
    experiments: (manifest.experiments as Artifact["experiments"]) ?? [],
    traces: readList(paths.traces ?? "traces.yml", "traces"),
    results: readList(paths.results ?? "results.yml", "results"),
    claims: readList(paths.claims ?? "claims.yml", "claims"),
    assessments: readList(
      paths.assessments ?? "assessments.yml",
      "assessments",
    ),
    paper: manifest.paper as Artifact["paper"],
    research_agent: manifest.research_agent as Artifact["research_agent"],
    reflection: existsSync(join(dir, "reflection.md"))
      ? readFileSync(join(dir, "reflection.md"), "utf-8")
      : undefined,
    journal: readList(paths.journal ?? "journal.yml", "journal"),
  };
  return a;
}
