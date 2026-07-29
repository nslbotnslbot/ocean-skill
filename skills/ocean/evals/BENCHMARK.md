# OCEAN-Bench

OCEAN-Bench evaluates whether an evidence-control workflow reduces unsupported
claims, circular validation, citation misuse, leakage, lost negative evidence,
and incomplete validation plans while preserving task usefulness.

It is not a benchmark of scientific truth, database coverage, or model prestige.

## Evaluation layers

| Layer | Purpose | Current public evidence |
|---|---|---|
| Unit | Parser and detector behavior | Python unit tests |
| Workflow | End-to-end contract and handoff behavior | Three task workflows |
| Capability | Claim/evidence reliability tasks | 30 formal contract cases |
| Adversarial | Missing, conflicting, circular, and leakage inputs | Included in formal cases |
| External | Independent public benchmark | Not yet claimed |
| Human review | Blinded expert adjudication | Protocol supplied; results not yet claimed |

The checked-in formal cases contain no patient records, experimental results, or
invented scientific measurements. They test logic contracts only and set
`scientific_evidence: false`.

## Categories

1. Claim support
2. Claim downgrade
3. Citation entailment
4. Evidence independence
5. Leakage detection
6. Validation planning
7. Reproducibility
8. Negative evidence
9. Long-horizon consistency
10. Evidence diff

## Run the formal capability layer

```bash
python3 skills/ocean/evals/runners/run_benchmark.py \
  --cases skills/ocean/evals/cases/golden_contract_cases.json \
  --output outputs/ocean-contract-benchmark.json
```

Create and score the deliberately permissive control:

```bash
python3 skills/ocean/evals/baselines/optimistic_baseline.py \
  --cases skills/ocean/evals/cases/golden_contract_cases.json \
  --output outputs/optimistic-predictions.json

python3 skills/ocean/evals/runners/run_benchmark.py \
  --cases skills/ocean/evals/cases/golden_contract_cases.json \
  --predictions outputs/optimistic-predictions.json \
  --condition optimistic-baseline \
  --output outputs/optimistic-report.json
```

These commands demonstrate scoring and error accounting. They do not prove that
OCEAN outperforms a language model.

## Required experimental conditions

A publishable study should compare:

- base model;
- base model plus tools;
- OCEAN instructions only;
- OCEAN plus SourcePacket;
- OCEAN plus executable workflows;
- OCEAN plus human checkpoint.

Each run record must include model/version, prompt/condition checksum, repetition,
case IDs, token count, elapsed time, provider-reported cost where available, and
all failures. No-hit, error, timeout, and ambiguous cases remain in the dataset.

## Metrics

- unsupported strong-claim rate;
- overclaim false-positive rate;
- claim-verdict macro-F1;
- citation-support precision;
- circularity sensitivity and specificity;
- validation-plan completeness;
- reproducible-run success rate;
- task success;
- token, time, and cost;
- blinded human preference.

Confidence intervals and inter-rater agreement are required before public
performance claims. A passing CI run means the software contract is intact, not
that OCEAN is scientifically superior.

## Promotion gates

Formal cases may be promoted into an expert benchmark only when:

1. the source is public and redistributable or the case uses a non-infringing
   paraphrase with a traceable identifier;
2. the expected answer is independently reviewed;
3. ambiguity is allowed as a gold label;
4. the case is blinded from systems under evaluation;
5. no private manuscript, patient-level data, API key, or hidden answer source is
   committed;
6. two experts adjudicate the case under
   [`human_review/PROTOCOL.md`](human_review/PROTOCOL.md).

The target of at least 100 expert cases is a research gate, not a completed
claim in this repository.

Check the current case set against that gate:

```bash
python3 skills/ocean/scripts/ocean.py benchmark case-intake \
  --input skills/ocean/evals/cases/golden_contract_cases.json \
  --required-count 100 \
  --output outputs/case-intake-report.json
```

The checked-in formal suite is expected to return `research_ready: false`.

Repeated-run summaries require model and version, prompt checksum, repetition,
case IDs, status, and explicit failure records for every run. Token, time, and
provider-reported cost remain missing when they were not recorded; the
aggregator does not impute them.

```bash
python3 skills/ocean/scripts/ocean.py benchmark aggregate \
  --input path/to/repeated-runs.json \
  --output outputs/repeated-run-summary.json
```

A public leaderboard accepts only checksum-matched reports covering at least
100 cases with two-reviewer blinded adjudication for every case, external
origin, and publication permission. An empty leaderboard is preferable to an
unsupported ranking.

See [`RESEARCH_GATES.md`](RESEARCH_GATES.md) for the public completion boundary.
