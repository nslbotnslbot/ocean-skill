# Sounding Multi-Model Strict Eval R1: DeepSeek and Gemini API Slice Results

Date: 2026-06-29
Status: executed for DeepSeek and Google Gemini API slices after local keys were configured.

## Execution Boundary

- Skill under test: `skills/ocean`.
- Runner: `skills/ocean/scripts/run_sounding_multimodel_eval.py`.
- Cases: `skills/ocean/evals/sounding-multimodel-cases.json`, SM1-SM5.
- Outputs: ignored runtime artifacts under `outputs/`, not intended for Git.
- API keys: loaded from `.env.ocean.local`; key values were not printed or written to tracked files.
- Scientific boundary: this validates OCEAN/Sounding behavior, not the scientific truth of the source packets.

## Provider Boundary

| Provider | Configured model | Lane | Notes |
|---|---|---|---|
| DeepSeek | `deepseek-v4-pro` | Open-weight reproducibility / API-hosted | Completed all five cases after the final prompt tightening. |
| Google Gemini | `gemini-2.5-flash` | Frontier ceiling / API-hosted | `gemini-3.5-flash` and `gemini-flash-latest` returned HTTP 503 during a minimal API ping, while `gemini-2.5-flash` succeeded and was used for this runnable slice. |

## Prompt/Runner Changes Before Final Runs

- Renamed the evidence-discovery workflow to Sounding in public-facing prompts and files.
- Added `--model-id`, `--case-id`, and `--case-limit` so small smoke tests can run before full evals.
- Added Google Gemini `generateContent` REST support alongside OpenAI-compatible chat completions.
- Tightened required heading instructions to exact lines:
  `一、Sounding检索任务定义`, `二、检索记录`, `三、候选来源表`, `四、Evidence Radar Map`, `五、Negative Space`, `六、Sounding边界`, `七、Handoff Ticket`, `八、Strict gate verdict`.
- Added compact-output constraints and output token caps to reduce oversized table generation.
- Expanded automatic boundary checks to recognize common Chinese/English synonyms for cannot judge, not inspected, needed next, and two-verdict-layer language.

## Final Run Artifacts

| Model | Ignored output directory | Cases completed |
|---|---|---:|
| DeepSeek `deepseek-v4-pro` | `outputs/sounding-multimodel-r1-deepseek-rerun/20260629-154402/` | 5 |
| Gemini `gemini-2.5-flash` | `outputs/sounding-multimodel-r1-gemini-rerun/20260629-153919/` | 5 |

## Final Enhanced Auto-Check Matrix

| Model | Case | Required headings | Cannot judge language | Not inspected language | Needed next language | Two verdict layers |
|---|---|---|---|---|---|---|
| DeepSeek | SM1 | Pass | Pass | Pass | Pass | Pass |
| DeepSeek | SM2 | Pass | Pass | Pass | Pass | Pass |
| DeepSeek | SM3 | Pass | Pass | Pass | Pass | Pass |
| DeepSeek | SM4 | Pass | Pass | Pass | Pass | Pass |
| DeepSeek | SM5 | Pass | Pass | Pass | Pass | Pass |
| Gemini | SM1 | Pass | Pass | Pass | Pass | Pass |
| Gemini | SM2 | Pass | Pass | Pass | Pass | Pass |
| Gemini | SM3 | Pass | Pass | Pass | Pass | Pass |
| Gemini | SM4 | Pass | Pass | Pass | Pass | Pass |
| Gemini | SM5 | Pass | Pass | Pass | Pass | Pass |

## Failure/Iteration Notes

- The first Gemini SM1 attempt with the `interactions` endpoint failed with HTTP 500. The runner was changed to the Gemini `generateContent` endpoint.
- A direct Gemini model ping showed `gemini-3.5-flash` and `gemini-flash-latest` returned HTTP 503, while `gemini-2.5-flash` returned successfully.
- The first Gemini full run completed 5/5 but SM3/SM4 had unstable formatting and oversized outputs. The prompt was tightened to require exact heading lines and compact tables. The final rerun passed all automatic checks.
- The first DeepSeek full run completed 5/5 but the older checker missed synonymous boundary wording in some cases. After prompt and checker tightening, the final DeepSeek rerun passed all enhanced automatic checks.

## Release Interpretation

This slice supports a limited release statement:

> Sounding Multi-Model Strict Eval R1 has now passed a live API slice for DeepSeek `deepseek-v4-pro` and Google Gemini `gemini-2.5-flash` across five source-boundary cases using the tightened Sounding output contract. This is a workflow and format-boundary validation, not a scientific truth validation.

Do not claim that Qwen, Kimi, MiniMax, Mistral, Llama, Claude, OpenAI API, or Perplexity retrieval control have passed this eval until their outputs are separately recorded.
