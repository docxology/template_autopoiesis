# Use the standalone generator

From the repository root, install Python 3.11 or later and uv, then use the
committed lockfile for the development environment.

```sh
uv sync --locked --python 3.13 --extra dev
uv run --no-sync python scripts/autopoiesis.py expand
uv run --no-sync python scripts/autopoiesis.py sample --count 5
uv run --no-sync python scripts/autopoiesis.py honesty
```

Edit `project_config.autopoiesis` in the
[live configuration](manuscript/config.yaml) to change the seed, grammar
slots, and vendored dependency choices. The default product has 360 nominal
cells and 45 effective cells. The remaining variation comes from three
reserved slots. The [grammar reference](SYNTAX.md) defines supported forms.

Generate and verify a child in a temporary output location:

```sh
child_dir="$(mktemp -d)"
uv run --no-sync python scripts/autopoiesis.py materialize --out-root "$child_dir"
uv run --no-sync python scripts/autopoiesis.py verify "$child_dir"/child_*
```

The child has its own primitive kernels, figure helper, tests, scripts, and
manuscript. Requested single-file infrastructure modules are copied when
available and otherwise emitted as stubs. The default grammar requests no
infrastructure dependencies. The `template` dependency mode raises an error.
Child builds are byte-stable within a matching Python and platform environment.
The parent manuscript uses the [shared renderer](manuscript-build.md).

Run the native test suite with the declared 90% branch-coverage gate:

```sh
uv run --no-sync pytest --cov=src --cov-branch --cov-fail-under=90 -q
```

Existing files in [output](../output/) are versioned reproducibility evidence,
including generated child trees, figures, and the rendered parent manuscript.
Generate fresh manuscript evidence in a disposable checkout.
