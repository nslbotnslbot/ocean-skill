# Common Tool Adapter Helpers

Common helpers are shared by tool-specific folders under `scripts/tools/`.

## Generic software source packet

Use `software_source_packet.py` when a tool has run metadata but no dedicated wrapper yet.

```bash
python3 scripts/tools/common/software_source_packet.py template \
  --tool-name FastQC \
  --tool-slug fastqc \
  --output fastqc-run-template.json

python3 scripts/tools/common/software_source_packet.py audit \
  --input fastqc-run.json \
  --output fastqc-run-audit.json

python3 scripts/tools/common/software_source_packet.py packet \
  --input fastqc-run.json \
  --output fastqc-source-packet.json
```

The helper does not run external software. It only checks provenance completeness and creates bounded OCEAN source packets from inspected run metadata.

