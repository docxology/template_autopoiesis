# SYNTAX.md — Grammar Syntax Reference

## Grammar Structure

The grammar is defined in `docs/manuscript/config.yaml` under the
`project_config.autopoiesis:` key (a top-level `autopoiesis:` fallback remains
for standalone forks created before that schema):

```yaml
project_config:
  autopoiesis:
    seed: 1618033        # integer — seeds all deterministic selections
    slots:               # shorthand mapping: slot name → list of options
      domain: [a, b, c]
      section_set: [x, y]
    deps: [logging, glossary_gen]  # list of vendorable dependency names
```

---

## Slot Format

Each slot can be written in two ways:

**Shorthand** (list value):
```yaml
slots:
  domain: [optimization, dynamics, statistics]
```

**Longhand** (in the `autopoiesis.slots` expanded config):
```yaml
slots:
  - name: primitive_domain
    options: [optimization, dynamics, statistics]
```

The `parse_grammar()` function normalizes both forms.

---

## Slot Table

| Slot name | Options | Reserved? |
|---|---|---|
| `primitive_domain` | optimization, dynamics, statistics, signal, graph | No |
| `track` | analytical, empirical, hybrid | No |
| `section_set` | minimal, standard, extended | No |
| `figure_profile` | minimal, full | **Yes** |
| `qr_profile` | off, on | **Yes** |
| `integrity_profile` | sha256, merkle | **Yes** |

Reserved slots are included in the nominal product size but are not varied in the effective product space.

---

## Product Calculation

- **Nominal product**: product of all slot option counts
- **Effective product**: product of non-reserved slot option counts
- **Inflation factor**: nominal / effective (reported honestly in abstract)

---

## Deps Syntax

```yaml
deps: [logging, glossary_gen]   # list of vendorable dependency names
```

Valid dep names: `logging`, `glossary_gen`, `figure_manager`, `manuscript_injection`, `steganography`.

`parse_grammar()` requires `deps` to be a list of these names; a mapping form
raises `GrammarError: Grammar deps must be a list`. The `template`/`vendor`
modes are selected later, at materialization time, not in the grammar block.

---

## CLI Usage

```bash
# Enumerate all grammar cells
python scripts/autopoiesis.py enumerate

# Expand to spec (default seed)
python scripts/autopoiesis.py expand

# Expand to spec (custom seed)
python scripts/autopoiesis.py expand --seed 999

# Sample N specs
python scripts/autopoiesis.py sample --count 10

# Materialize
python scripts/autopoiesis.py materialize --out-root /tmp/children

# Verify
python scripts/autopoiesis.py verify /tmp/children/child_optimization_XXXX

# Honesty check
python scripts/autopoiesis.py honesty
```

---

## Grammar Hash

The grammar hash is the first 16 hex characters of SHA-256 of the canonical JSON:

```python
canonical = json.dumps(
    {
        "seed": seed,
        "slots": [{"name": name, "options": options}, ...],
        "deps": [...],
        "archetype_filters": {name: options, ...},
    },
    sort_keys=True, separators=(',', ':')
)
grammar_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]
```

A change to any slot name, option, dep, or archetype filter changes the
grammar hash.

---

## Common Errors

| Error | Cause |
|---|---|
| `GrammarError: must define at least one slot` | `slots:` key is empty or missing |
| `GrammarError: must have ≥1 option` | A slot has an empty options list |
| `GrammarError: duplicate options` | A slot has repeated option values |
| `GrammarError: Unknown dep` | A dep name is not in `VENDORABLE_DEPS` |
| `GrammarError: Grammar block must be a mapping` | Non-dict passed to `parse_grammar` |
