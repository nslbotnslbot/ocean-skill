# Evidence Boundary Gate

Every substantive OCEAN output must establish the evidence boundary before making strong judgments.

Use these four labels exactly:

- 已检查:
- 未检查:
- 不能判断:
- 下一步需要:

## Boundary rules

- If only a title, abstract, idea sentence, meeting note, source summary, DOI page, or database name is available, keep the answer at that evidence level.
- If a full text, data table, figure, supplement, code repository, API response, or public review file was not inspected, say so.
- If a source was mentioned by the user but not opened or queried, treat it as unverified context.
- If live search or database access is unavailable, say that OCEAN can only work from provided materials.
- If a model/API retrieves external context during the answer, separate it from packet evidence using `retrieved external context`.

## Stop conditions

Stop or downgrade when:

- concrete identifiers are requested but no real query/API response is provided;
- clinical readiness is requested without prospective, external, or implementation evidence;
- reproducibility is claimed from file names without code, data, environment, and parameters;
- manuscript submission status is requested without an explicit submission record;
- authorship/contribution status is requested without a written record;
- a trend judgment is requested without a search corpus or cited source packet;
- mechanism/causality is requested from association, annotation, text mining, docking, or model prediction alone.
