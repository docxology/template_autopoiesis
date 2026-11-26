# Build Autopoietic Project Generation

Install Git, uv, Pandoc 3.14 with pandoc-crossref 0.3.26b, XeLaTeX with the
[required TeX packages](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/usage/output-formats.md)
(including `fontsize`). The three [Mermaid diagram assets](manuscript/figures/README.md)
are checked in with their source.

From a clean project checkout, make a disposable copy at the exact committed
revision. The commands use the project's locked dev environment for
measurements and the separate renderer environment for stages 03 and 04.

```sh
set -e
project_root="$(pwd -P)"
work_directory="$(mktemp -d)"
renderer="$work_directory/template"
git clone https://github.com/docxology/template.git "$renderer"
git -C "$renderer" checkout --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
mkdir -p "$renderer/projects/working"
project_copy="$renderer/projects/working/template_autopoiesis"
git clone --no-hardlinks "$project_root" "$project_copy"
git -C "$project_copy" checkout --detach "$(git -C "$project_root" rev-parse HEAD)"

cd "$renderer"
uv sync --locked --no-dev
cd "$project_copy"
uv sync --locked --python 3.13 --extra dev
export PYTHONPATH="$renderer${PYTHONPATH:+:$PYTHONPATH}"
uv run --no-sync python scripts/02_measure_test_coverage.py
uv run --no-sync python scripts/01_generate_manuscript_assets.py
uv run --no-sync python scripts/generate_cover_art.py
uv run --no-sync python scripts/z_generate_manuscript_variables.py

cd "$renderer"
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/template_autopoiesis --skip-manuscript-hydration
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/template_autopoiesis
```

The preparation commands measure coverage, generate the four registered
manuscript figures and the cover, stage the three authored diagrams, and hydrate `output/manuscript/` from
[the authored sections](manuscript/README.md). The full analysis allowlist
also materializes and seals child projects. The focused parent manuscript
build uses the four preparation scripts above. Stage 03 consumes the hydrated
copy prepared with the project's locked Python environment.

Inspect `output/pdf/template_autopoiesis_combined.pdf`, `output/web/index.html`,
and the validation and provenance receipts in `output/reports/` inside the
disposable copy. Compare the coverage figure to
`output/data/coverage_full.json` from that same run.
