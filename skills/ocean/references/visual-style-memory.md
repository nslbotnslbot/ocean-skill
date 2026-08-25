# Visual Style Memory

This reference records reusable visualization preferences for OCEAN outputs that include
charts, trend maps, scorecards, pathway maps, score matrices, and comparison figures.

## Purpose

- Keep OCEAN visual outputs stylistically consistent across modules.
- Separate stylistic choices from scientific evidence strength.
- Preserve accepted/rejected style traits for later requests.

## Default Profiles

Each profile is a reusable ID and can be switched explicitly by user request.

### `ocean-glacier-lite`
- palette: `#0b2a4f`, `#6d8ea8`, `#9fb5ca`, `#e3edf6`, `#f5a623`
- typography: sans-serif, medium weight titles, tighter line spacing
- lines: 1.5px, low chart clutter, subtle grid (0.30 alpha)
- legend: outside-right, compact, one-line labels
- annotation: short labels; avoid dense callouts
- background: white or very light slate
- intended use: trend maps, direction maps, scorecards, summary visuals

### `ocean-editorial-review`
- palette: `#1b2a44`, `#3d5a80`, `#98c1d9`, `#ee6c4d`, `#293241`
- typography: strong heading contrast, concise axis labels
- lines: 1.4px, readable but not heavy
- legend: above-right when density is low, otherwise bottom compact
- annotation: one-line rationale only
- background: off-white or white
- intended use: comparison tables, decision cards, review visuals

### `ocean-plain`
- palette: `#1f2937`, `#4b5563`, `#9ca3af`, `#d1d5db`, `#111827`
- typography: neutral, high readability, minimal decoration
- lines: thin, sparse
- legend: stable bottom row
- annotation: minimal but explicit
- background: white
- intended use: clinical/biological dense data visuals and compact plots

### `ocean-biomed-accent`
- palette: `#082f49`, `#0ea5e9`, `#14b8a6`, `#f59e0b`, `#f97316`
- typography: clean sans-serif, explicit labels, medium-high contrast
- lines: 1.3px, light major grid and visible minor grid
- legend: top-right or right side, compact rows
- annotation: short explanatory notes, one sentence max
- background: white
- intended use: biomed benchmark comparisons, pathway maps, mechanism summaries

## Learning Model (v1)

OCEAN treats visual style as accumulated preference:

- 项目级记忆：同一 `project_id` 的下一次可视化先复用该项目最新确认通过的 profile。
- 模块级记忆：未命中项目记忆时，优先复用模块级最近有效 profile（例如 Sounding / Current / Reef ...）。
- 图形类型记忆：未命中项目和模块记忆时，按图形类型（trend-map/scorecard/heatmap/radar）复用历史偏好，保持风格连续性。
- 学习反馈：在用户接受、部分接受、拒绝时更新 profile 评分；
  - accepted = +2
  - partially_accepted = +1
  - rejected = -2
  - pending = 0
- 趋势回放：`learning` 统计会保留 profile 的累积偏好、关键接受/拒绝特征点（palette、legend、annotation 等）。
- 风险边界：拒绝不等于停止；会改为 `partially_accepted` / `rejected` 标记，并要求下一次请求确认。

## Default Memory Fields

For mixed-visual workflows (e.g., scorecard + volcano + network), use one `stylebook` plan first, then close each figure with `style-session --action close`. This keeps one session-wide direction while preserving per-artifact feedback.

Track these fields in Harbor records for each visualization workflow:

- `visual_style_profile_id`
- `last_changed` (date)
- `accepted_aspects` (palette, spacing, annotation, etc.)
- `rejected_aspects`
- `next_tuning_request`

## Machine Memory Record

The canonical JSON style catalog is:

- `references/visual-style-memory.json`

Runtime memory can be managed with:

```bash
python3 scripts/runtime/visual_style_memory.py init
python3 scripts/runtime/visual_style_memory.py style-session --project-id <project_id> --module <module> --artifact-type <artifact_type> --action open
python3 scripts/runtime/visual_style_memory.py suggest --project-id <project_id> --module <module> --artifact-type <artifact_type>
python3 scripts/runtime/visual_style_memory.py export --project-id <project_id> --module <module> --artifact-type <artifact_type> --format python
python3 scripts/runtime/visual_style_memory.py harbor-card --project-id <project_id> --module <module> --artifact-type <artifact_type> --feedback accepted|partially_accepted|rejected|pending
python3 scripts/runtime/visual_style_memory.py record \
  --project-id <project_id> --module <module> --artifact-type <artifact_type> --profile-id <profile_id> --feedback accepted|partially_accepted|rejected|pending
python3 scripts/runtime/visual_style_memory.py report --project-id <project_id> --module <module> --artifact-type <artifact_type>
python3 scripts/runtime/visual_style_memory.py portfolio --project-id <project_id> --module <module> --artifact-type <artifact_type>
python3 scripts/runtime/visual_style_memory.py audit --project-id <project_id> --module <module> --artifact-type <artifact_type>
python3 scripts/runtime/visual_style_memory.py stylebook --project-id <project_id> --module <module> --artifact-types volcano,manhattan,clustermap
```

Recommended use:

- record style feedback every time user explicitly accepts or rejects a generated visual;
- close the workflow with `harbor-card` after each visual artifact is produced, so Harbor can replay style context next time.
- For many figures in one workflow, keep one compact style snapshot using:
  `python3 scripts/runtime/visual_style_memory.py export --project-id <project_id> --module <module> --format summary` or
  `python3 scripts/runtime/visual_style_memory.py portfolio --project-id <project_id> --module <module> --artifact-type <artifact_type>`.
- keep `visual_style_feedback` in Harbor artifact entries as `accepted`, `partially_accepted`,
  `rejected`, or `pending`;
- use `--format python` to generate reusable plotting boilerplate when you actually create matplotlib/seaborn figures.
- reuse the resolved profile for the same `project_id` in the next visualization request unless
  a new profile is explicitly selected.

Suggested closed loop for visual work:

1. `style-session --action open` -> pick profile and pending harbor card.
2. apply style and generate the chart/figure.
3. `style-session --action close` -> feedback and Harbor-ready metadata are persisted automatically for accepted / partially_accepted / rejected by default.
4. `accepted` and `partially_accepted` will
   become the active style memory for the same project/module/artifact type; `rejected` keeps style memory as-is and records boundary feedback.
5. `portfolio` -> review module/project style trajectory.
6. `growth` -> generate a compact style-growth report across project/module/artifact dimensions before the next batch.
7. `audit` -> generate focused quality checks within one slice when needed.

### Common artifact types

建议在 `--artifact-type` 用稳定短标签（建议 1-2 词）：

- `trend-map`
- `scorecard`
- `heatmap`
- `radar`
- `network`
- `roc`
- `pr-curve`
- `volcano`
- `bar`
- `violin`
- `scatter`
- `boxplot`
- `forest`
- `funnel`
- `confusion-matrix`
- `correlation-matrix`
- `upset`
- `sankey`
- `time-series`
- `pathway`
- `sensitivity`
- `histogram`
- `density`
- `pie`
- `qq`
- `embedding`（UMAP/t-SNE/PCA）
- `survival`
- `dotplot`
- `area`
- `waterfall`
- `sunburst`
- `alluvial`
- `manhattan`
- `clustermap`
- `dendrogram`
- `lollipop`
- `ridge`
- `ma-plot`
- `boxen`
- `errorbar`
- `circos`
- `chord-diagram`
- `treemap`
- `wordcloud`
- `heat-tree`

如果同一类型反复出现，优先按类型记忆复用；类型更换时建议保留上一次的
`artifact_type`、`visual_style_feedback`，并在接下来一次可视化前确认是否切换风格。

### Artifact-type auto normalization

To keep memory stable across different user wording, OCEAN now normalizes frequent aliases:

- `line chart`, `line`, `trend`, `trend map` -> `trend-map`
- `score`, `score card` -> `scorecard`
- `heat`, `heat map` -> `heatmap`
- `roc`, `roc curve`, `pr`, `precision-recall`, `ROC曲线`, `PR曲线` -> `roc` / `pr-curve`
- `umap`, `t-SNE`, `PCA` -> `embedding`
- `火山图`, `曼哈顿图`, `散点图`, `箱线图`, `生存曲线`, `误差线` -> mapped aliases
- `volcano plot`, `confusion`, `correlation matrix`, `time series`, `sankey` -> canonical names above
- `manhattan plot`, `ma plot`, `clustermap`, `clustermap`, `heat-tree`, `lollipop`, `ridge plot`, `dendrogram` -> mapped aliases

You can also pass raw user phrasing such as `linechart`, `line_` variations, `score card`, `time series` and they are normalized automatically by
`scripts/runtime/visual_style_memory.py`.

### Aesthetic growth audit (new)

For a larger project, use `audit` to avoid drifting into a single style profile:

```bash
python3 scripts/runtime/visual_style_memory.py audit \
  --project-id <project_id> \
  --module <module> \
  --artifact-type <artifact_type> \
  --feedback accepted
```
or
```bash
python3 scripts/runtime/visual_style_memory.py growth \
  --project-id <project_id> \
  --module <module> \
  --artifact-type <artifact_type>
```
```bash
python3 scripts/runtime/visual_style_memory.py stylebook \
  --project-id <project_id> \
  --module <module> \
  --artifact-types <artifact-type-1,artifact-type-2,...>
```

`stylebook` gives a compact cross-artifact preference summary before a design batch:
- recommended profile per requested artifact type
- recent resolved style
- acceptance_rate and top profile trend
- learning context by project/module

`growth` now reports weighted preference and momentum:
- weighted preference uses `accepted=+2`, `partially_accepted=+1`, `rejected=-2`, `pending=0`
- `style_momentum` compares recent vs prior feedback score windows for each artifact type
```

Interpret the report as trend control rather than proof:

- acceptance_rate is the ratio of accepted + partially accepted events;
- `top_artifact_profile_pairs` shows which profile works best in each artifact bucket;
- `recent_events` is your immediate memory for next-session continuity.
- `growth` adds module and project trajectory rows so different visualization families can still share one profile.

If your tag is still not in the canonical list, OCEAN keeps it as-is and still learns from feedback.

### Default profile routing by artifact family

For new visualizations before explicit feedback, OCEAN uses family defaults as an initial suggestion:

| Artifact family | Initial profile |
|---|---|
| `trend-map`, `time-series`, `bar`, `scatter` | `ocean-glacier-lite` |
| `scorecard`, `radar`, `roc`, `pr-curve`, `forest`, `funnel`, `confusion-matrix` | `ocean-editorial-review` |
| `heatmap`, `correlation-matrix`, `violin`, `boxplot`, `upset` | `ocean-plain` |
| `network`, `pathway`, `sensitivity`, `sankey` | `ocean-biomed-accent` |

This routing is only a starting point. User feedback through `record` still drives long-term preference.

## Update Rules

1. Use an existing profile ID when no explicit new preference is requested.
2. If user rejects a profile, record rejected traits and prefer a neighboring profile.
3. If user gives a new preference, request one of the existing profiles explicitly
   (for example `--requested-profile`) and record feedback to reinforce that preference.
4. Do not invent user preferences; only record what was explicitly stated or accepted.
5. Visual style is for clarity and trust, not persuasive exaggeration.

## Cross-Module Mapping

When output includes figures or maps, add metadata in Harbor artifacts:

- `visual_style_profile_id`
- `visual_style_traits`
- `visual_style_feedback`
