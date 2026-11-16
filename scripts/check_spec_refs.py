#!/usr/bin/env python3
"""Check cross-references in the specifications.

Checks, in SPEC.md (SDK), docs/judge-reviewer-spec (JR), and docs/artifact-explorer-spec
(explorer):

- every section reference (``§3.1``, ``JR §6.7``, ``SDK §2.4.1``) names a heading that exists
  in the referenced document set. A bare ``§`` refers to the document set it appears in;
  ``JR``, ``SDK`` and ``explorer`` prefixes switch sets, and a prefix carries over a range
  (``JR §6.1–§6.3``) and a list (``JR §1.2 and §6.4``, ``SDK §2.6, §2.7``);
- a reference that names an explorer route (``route `#/…`, §5.3``) cites §5.3, which
  defines every route;
- ``§N item K`` / ``§N rule K`` names a numbered list item that exists in that section;
- scenario IDs (``X12`` in the explorer, ``JR J9``) and explorer invariants (``I6``) exist.

References to external documents (``RFC 3986 §5.2.4``, ``` `evaluable-artifact/v1` §1.1 ```)
are skipped. Exits 1 and lists every
broken reference when any is found. Standard library only.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADING = re.compile(r"^(#{1,6})\s+(\d+(?:\.\d+)*)\.?\s")
NUMBERED_ITEM = re.compile(r"^\s*(\d+)\.\s")
# One reference run: an optional prefix, a first section, then any number of
# range / list continuations whose sections are bare.
SECTION = r"§(\d+(?:\.\d+)*)"
# External documents (an RFC, a named format version in backticks) are recognized so that
# they can be skipped.
PREFIX = r"(?:(RFC\s+\d+|`[^`\n]+/v\d+`|JR|SDK|explorer)\s+)?"
CONTINUATION = r"(?:\s*(?:–|-|,|and|or|/)\s*" + SECTION + r")"
REF_RUN = re.compile(PREFIX + SECTION + r"((?:" + CONTINUATION + r")*)")
CONT_SECTION = re.compile(SECTION)
ITEM_AFTER = re.compile(r"\s+(item|rule)\s+(\d+)")
# A section number can exist and still be the wrong target. Where a reference names a thing
# that one section defines, it must cite that section: an explorer route (`#/…`) is defined
# by the routes table of §5.3.
ROUTE_REF = re.compile(r"routes?\s+`#/[^`]*`[^()§]{0,60}§(\d+(?:\.\d+)*)")
ROUTES_SECTION = "5.3"
SCENARIO_DEF = re.compile(r"^\|\s*([XJ]\d+)\s*\|", re.M)
INVARIANT_DEF = re.compile(r"^\|\s*(I\d+)\s*\|", re.M)


@dataclass
class DocSet:
    name: str
    files: list[Path]
    sections: dict[str, str] = field(default_factory=dict)  # number -> body text
    scenarios: set[str] = field(default_factory=set)
    invariants: set[str] = field(default_factory=set)

    def load(self) -> None:
        for path in self.files:
            text = path.read_text(encoding="utf-8")
            self.scenarios |= set(SCENARIO_DEF.findall(text))
            self.invariants |= set(INVARIANT_DEF.findall(text))
            current: str | None = None
            body: list[str] = []
            in_fence = False
            for line in text.splitlines():
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                match = None if in_fence else HEADING.match(line)
                if match:
                    if current is not None:
                        self.sections[current] = "\n".join(body)
                    current, body = match.group(2), []
                elif current is not None:
                    body.append(line)
            if current is not None:
                self.sections[current] = "\n".join(body)


def doc_sets() -> dict[str, DocSet]:
    sets = {
        "SDK": DocSet("SDK", [ROOT / "SPEC.md"]),
        "JR": DocSet("JR", sorted((ROOT / "docs/judge-reviewer-spec").glob("[0-9]*.md"))),
        "explorer": DocSet(
            "explorer", sorted((ROOT / "docs/artifact-explorer-spec").glob("[0-9]*.md"))
        ),
    }
    for doc in sets.values():
        doc.load()
    return sets


def has_item(body: str, number: int) -> bool:
    return any(
        (m := NUMBERED_ITEM.match(line)) and int(m.group(1)) == number
        for line in body.splitlines()
    )


def check(sets: dict[str, DocSet]) -> list[str]:
    errors: list[str] = []
    for home in sets.values():
        for path in home.files:
            rel = path.relative_to(ROOT)
            text = path.read_text(encoding="utf-8")
            # Scan the whole file so that a prefix at the end of one line still applies
            # to a section number wrapped onto the next.
            for run in REF_RUN.finditer(text):
                lineno = text.count("\n", 0, run.start()) + 1
                prefix = run.group(1)
                if prefix and not prefix.startswith(("JR", "SDK", "explorer")):
                    continue
                target = sets[prefix] if prefix else home
                numbers = [run.group(2)] + CONT_SECTION.findall(run.group(3) or "")
                for number in numbers:
                    if number not in target.sections:
                        errors.append(f"{rel}:{lineno}: {target.name} §{number} does not exist")
                item = ITEM_AFTER.match(text[run.end():])
                last = numbers[-1]
                if item and last in target.sections:
                    if not has_item(target.sections[last], int(item.group(2))):
                        errors.append(
                            f"{rel}:{lineno}: {target.name} §{last} has no "
                            f"{item.group(1)} {item.group(2)}"
                        )
            if home.name == "explorer":
                for ref in ROUTE_REF.finditer(text):
                    if ref.group(1) != ROUTES_SECTION:
                        lineno = text.count("\n", 0, ref.start()) + 1
                        errors.append(
                            f"{rel}:{lineno}: a route is defined in §{ROUTES_SECTION}, "
                            f"not §{ref.group(1)}"
                        )
            for lineno, line in enumerate(text.splitlines(), 1):
                errors.extend(check_ids(home, sets, rel, lineno, line))
    return errors


def check_ids(
    home: DocSet, sets: dict[str, DocSet], rel: Path, lineno: int, line: str
) -> list[str]:
    errors: list[str] = []
    if home.name == "explorer":
        for sid in re.findall(r"(?<![\w-])(X\d+)\b", line):
            if sid not in home.scenarios:
                errors.append(f"{rel}:{lineno}: explorer scenario {sid} does not exist")
        for inv in re.findall(r"(?<![\w-])(I\d+)\b(?! there)", line):
            if inv not in home.invariants:
                errors.append(f"{rel}:{lineno}: explorer invariant {inv} does not exist")
    for jid in re.findall(r"\bJR\s+(J\d+)\b", line):
        if jid not in sets["JR"].scenarios:
            errors.append(f"{rel}:{lineno}: JR scenario {jid} does not exist")
    if home.name == "JR":
        for jid in re.findall(r"(?<![\w-])(J\d+)\b", line):
            if jid not in home.scenarios:
                errors.append(f"{rel}:{lineno}: JR scenario {jid} does not exist")
    return errors


def main() -> int:
    sets = doc_sets()
    errors = check(sets)
    for error in errors:
        print(error)
    counted = {name: len(doc.sections) for name, doc in sets.items()}
    print(f"checked section references against {counted}: {len(errors)} broken")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
