# OCEAN Tool Adapters

This directory contains tool-specific source-packet adapters.

Each tool adapter should stay narrow:

- fetch or import source material;
- analyze only inspected files or API responses;
- create an OCEAN source packet;
- preserve what the packet cannot support.

Adapters do not decide scientific truth. OCEAN modules audit the resulting packet.

## Current layout

| Folder | Purpose |
|---|---|
| `alphafold_db/` | AlphaFold DB predicted-structure confidence and PAE source packets |
| `literature/` | PubMed, EuropePMC, or local literature metadata source packets |
| `clinicaltrials/` | ClinicalTrials.gov registry source packets |

Shared or cross-tool eval runners may live directly under `scripts/tools/`.

## Naming pattern

Prefer:

```text
scripts/tools/<tool_or_resource>/source_packet.py
scripts/tools/<tool_or_resource>/run_eval.py
```

Use tool-specific names only when a directory contains multiple independent adapters.

