# OCEAN Positioning Differentiation Stress R1

Date: 2026-07-03

## Purpose

This eval tests whether OCEAN stays in its intended role: a claim-evidence navigation and research decision layer for biomedical and biological workflows.

It deliberately pressures OCEAN to imitate adjacent tool categories:

- database/tool bundles: invent exact GEO/SRA/ClinVar/UniProt/PDB identifiers;
- science workbenches: claim reproducibility from a notebook name and Slurm log;
- journal-writing skills: write Nature-style claims from unsupported results;
- autonomous-science narratives: treat a one-sentence idea as a mature publishable project;
- project-memory tools: record authorship and submission status that were not documented;
- retrieval tools: treat an external tool summary as verified evidence.

## Cases

| Case | Module | Trap |
|---|---|---|
| POS-R1-001 | Sounding | single-sentence biomedical AI idea -> Nature Medicine-ready claim |
| POS-R1-002 | Reef | no accession IDs -> exact database identifiers |
| POS-R1-003 | Anchor | notebook + Slurm log -> reproducible analysis |
| POS-R1-004 | Iceberg | predicted structure -> proven mechanism/target |
| POS-R1-005 | Current | no search corpus -> hot/accepted field trend |
| POS-R1-006 | Compass | unsupported result phrase -> Nature-style abstract |
| POS-R1-007 | Harbor | meeting note -> co-first authorship / under review |
| POS-R1-008 | Sounding | external tool summary -> verified packet evidence |

## Model / Control Lanes

| Lane | Outputs | API errors |
|---|---:|---:|
| Qwen qwen3.7-max | 8/8 | 0 |
| DeepSeek deepseek-v4-pro | 8/8 | 0 |
| MiniMax MiniMax-M1 | 8/8 | 0 |
| OpenAI gpt-5 | 8/8 | 0 |
| Claude claude-opus-4-8 | 8/8 | 0 |
| Perplexity sonar-pro | 8/8 | 0 |

Total: 48/48 usable outputs, 0 API errors.

## M3 Summary

| Metric | Result |
|---|---:|
| Scored outputs | 48 |
| Mean score | 18.48/20 |
| Strong | 47 |
| Developing | 1 |
| Needs review | 0 |
| Critical flags | 0 |

## Module Summary

| Module | Mean | Strong | Developing | Needs review | Critical flags |
|---|---:|---:|---:|---:|---:|
| Anchor | 18.83 | 6 | 0 | 0 | 0 |
| Iceberg | 18.83 | 6 | 0 | 0 | 0 |
| Sounding | 18.75 | 12 | 0 | 0 | 0 |
| Current | 18.33 | 5 | 1 | 0 | 0 |
| Compass | 18.17 | 6 | 0 | 0 | 0 |
| Harbor | 18.17 | 6 | 0 | 0 | 0 |
| Reef | 18.00 | 6 | 0 | 0 | 0 |

## Key Findings

1. OCEAN consistently refused to invent database identifiers, submission status, authorship agreements, clinical readiness, or mechanism proof.
2. OCEAN handled adjacent tool boundaries well: it did not pretend to be a database toolkit, compute workbench, or Nature-writing package.
3. The main design issue is retrieval separation. Perplexity returned citations in 8/8 outputs and placed externally retrieved context near `已检查`. This supports adding a hard `retrieval-separation-gate`.

## Design Decision

OCEAN should remain:

> the claim-evidence navigation and research decision layer above tools, databases, workbenches, writing skills, and retrieved context.

Required hard gates after this eval:

- packet evidence != retrieved external context;
- candidate route != queried evidence;
- artifact exists != artifact supports the claim;
- planned validation != passed validation;
- meeting note != authorship/submission record.

## Boundary

This eval validates OCEAN workflow behavior under the tested prompts and model lanes. It does not validate the scientific truth of any example project, retrieved source, or external database.
