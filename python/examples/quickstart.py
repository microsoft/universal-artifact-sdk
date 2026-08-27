"""Create a minimal evaluable artifact.

Run from the repository root with ``python python/examples/quickstart.py``; the
submission is written to ``./out``.
"""

from universal_artifact_sdk import (
    AttestValidator,
    Claim,
    Result,
    add_claim,
    add_result,
    create_artifact,
    set_reflection,
    write_submission,
)

artifact = create_artifact(id="expt-42", title="Feedback-driven contraction")
add_claim(
    artifact,
    Claim(
        id="C1",
        statement="Feedback improves contraction",
        validators=[AttestValidator(checks="provenance", inputs=["R1"])],
    ),
)
add_result(
    artifact,
    Result(id="R1", validates=["C1"], evidence="results.csv", kind="metrics"),
)
set_reflection(artifact, "# Reflection\n\nThe corpus is small.\n")

report = write_submission(artifact, "out")
print(f"wrote {len(report.files_written)} files to {report.out_dir}")
if report.missing_blobs:
    print(f"still missing: {', '.join(report.missing_blobs)}")
