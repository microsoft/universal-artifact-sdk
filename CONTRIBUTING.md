# Contributing

This project welcomes contributions and suggestions.

## Contributor License Agreement

Most contributions require you to agree to a Contributor License Agreement (CLA)
declaring that you have the right to, and actually do, grant us the rights to use your
contribution. For details, visit <https://cla.opensource.microsoft.com>.

When you submit a pull request, a CLA bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., status check, comment). Simply
follow the instructions provided by the bot. You will only need to do this once across
all repositories using our CLA.

## Code of Conduct

This project has adopted the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the
[Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact
[opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or
comments.

## Development

```bash
npm ci                         # install Node dependencies
npm run typecheck
npm run build                  # tsc -> dist/
npm test                       # vitest (132 tests)

python -m pip install -e ".[dev]"
python -m pytest python/tests  # pytest (499 passed, 22 skipped)
python -m mypy                 # strict; configured in pyproject.toml
python -m ruff check python parity

npm run test:parity            # shared corpus + bidirectional cross-open
```

Please ensure the TypeScript and Python checks above pass before opening a pull request.
Build Python distributions with `python -m build --outdir dist-python`; never put
Python build products in `dist/`, which belongs to npm.

New behavior should be covered by tests in both bindings. Cross-binding behavior also
needs a reviewed case in [`parity/cases`](parity/cases): each case is language-neutral
data, its `expected` block is human-reviewed contract data, and no runner may derive an
expectation from a binding's current output. See
[`parity/expected/README.md`](parity/expected/README.md) for the review protocol,
[`PYTHON_BINDING.md`](PYTHON_BINDING.md) for the binding design, and
[`SPEC.md`](SPEC.md) for the format contract that the SDK implements.

The TypeScript API and implementation under `src/` are frozen while an experiment depends
on their behavior: do not change them. Contract inconsistencies found while working on
the Python binding are tracked in
[issue #32](https://github.com/microsoft/universal-artifact-sdk/issues/32).

## Trademarks

This project may contain trademarks or logos for projects, products, or services.
Authorized use of Microsoft trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks).
Use of Microsoft trademarks or logos in modified versions of this project must not cause
confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos is
subject to those third parties' policies.
