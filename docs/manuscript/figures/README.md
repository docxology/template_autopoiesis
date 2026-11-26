# Manuscript diagrams

The manuscript uses raster versions of the three authored Mermaid diagrams.
[Generation pipeline](generation-pipeline.mmd) shows the spec and provenance
flow. [Grammar product](grammar-product.mmd) illustrates the shipped grammar
with 45 effective and 360 nominal cells. [Generation methods](generation-methods.mmd)
shows the five analysis stages. Update the example diagram's labels when
changing the grammar. The paper's measurement tables use the live configuration.

With Mermaid CLI 12.2.0 and its Chrome Headless Shell 156.0.8078.47 installed,
run these commands from this directory after editing the diagrams:

```sh
mmdc --input generation-pipeline.mmd --output generation-pipeline.png
mmdc --input grammar-product.mmd --output grammar-product.png
mmdc --input generation-methods.mmd --output generation-methods.png
```

The [manuscript build](../../manuscript-build.md) stages the checked-in diagrams
alongside the generated figures in `output/figures/`.
