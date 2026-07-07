# API / Database Adapters

OCEAN includes bounded Reef adapters for public biomedical databases. These are real Python API wrappers: they construct official public API requests, optionally execute them, write JSON/Markdown Reef packets, and preserve evidence boundaries.

## Supported R1 Adapters

| Adapter | Resource | Required input | Can support | Cannot support alone |
|---|---|---|---|---|
| `uniprot` | UniProt | `--accession` or `--query` | protein metadata, accession, reviewed status, organism, annotation provenance | new function, mechanism, clinical utility |
| `pubmed` | PubMed via NCBI E-utilities | `--query` | PubMed record discovery and identifier provenance | full-paper evidence, mechanism, clinical efficacy |
| `europepmc` | Europe PMC | `--query` | literature metadata and abstract-level discovery | full-paper quality or peer-review outcome unless inspected |
| `chembl` | ChEMBL | `--query` | molecule metadata and ChEMBL identifier provenance | efficacy, safety, mechanism, clinical readiness |
| `opentargets` | Open Targets | `--ensembl-id` | target metadata and association-resource provenance | mechanism or therapeutic efficacy from association scores |
| `string` | STRING | `--identifier` or `--query` | identifier mapping / association-resource provenance | direct physical binding, mechanism, disease relevance |
| `reactome` | Reactome | `--query` | pathway/resource discovery provenance | pathway activity or causal disease mechanism |
| `quickgo` | QuickGO | `--query` | GO term metadata and annotation-resource provenance | direct molecular mechanism or phenotype proof |
| `clinvar` | ClinVar via NCBI E-utilities | `--query` | ClinVar record discovery and identifier provenance | diagnosis, treatment, pathogenicity without inspected details |
| `gnomad` | gnomAD GraphQL | `--variant-id` | population-frequency resource provenance | pathogenicity, diagnosis, actionability |
| `alphafold-db` | AlphaFold DB | `--accession` or `--query` | predicted-structure metadata provenance | experimental structure proof, binding, druggability |
| `clinicaltrials` | ClinicalTrials.gov | `--query` | registry status/design metadata provenance | treatment efficacy or clinical guidance |
| `ncbi-eutils` | NCBI E-utilities | `--database` and `--query` | Entrez record discovery and public metadata routing | full evidence, mechanism, causality, absence-of-evidence claims |

## Per-Resource Tool Folders

The same adapters are also exposed as science-skills-style tool folders under:

```text
skills/ocean/scripts/tools/databases/<adapter_slug>/
```

Each folder includes:

- `README.md`
- `api.json`
- `tool.json`
- `adapter_config.json`
- `examples/query.example.json`
- `scripts/query_packet.py`

The per-folder script delegates to `scripts/run_reef_api_adapter.py`, so adapter behavior stays centralized while each resource remains discoverable as a tool-library entry.

## Usage

Dry-run by default:

```bash
python3 skills/ocean/scripts/run_reef_api_adapter.py \
  --adapter uniprot \
  --accession P04637 \
  --out outputs/uniprot-packet.json
```

Bounded live request:

```bash
python3 skills/ocean/scripts/run_reef_api_adapter.py \
  --adapter alphafold-db \
  --accession P04637 \
  --execute \
  --retmax 1 \
  --out outputs/alphafold-db-packet.json
```

Run the adapter eval:

```bash
python3 skills/ocean/scripts/run_api_database_adapter_eval.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals
```

Run the per-resource database tool-folder eval:

```bash
python3 skills/ocean/scripts/tools/run_database_tool_adapter_eval.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals
```

Live eval requires network access:

```bash
python3 skills/ocean/scripts/run_api_database_adapter_eval.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals \
  --execute-live \
  --retmax 1
```

Per-resource live eval:

```bash
python3 skills/ocean/scripts/tools/run_database_tool_adapter_eval.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals \
  --execute-live \
  --retmax 1
```

## Evidence Boundary

These adapters inspect public API metadata only. They do not submit private manuscript text, patient data, PHI, unpublished data, or local omics files. A successful API response can support resource provenance, identifiers, public metadata, and database-routing decisions. It cannot by itself prove biological mechanism, causal inference, clinical utility, therapeutic efficacy, diagnosis, publication readiness, or reproducibility.

Use the resulting Reef packet as input to Iceberg, Anchor, Compass, or Harbor. Do not treat it as primary experimental validation.
