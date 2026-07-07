#!/usr/bin/env python3
"""Generate OCEAN database adapter folders.

The generated folders are lightweight wrappers around scripts/run_reef_api_adapter.py.
They make database resources visible as tool-library entries without duplicating
the Reef adapter implementation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent
from typing import Any


DATABASES: list[dict[str, Any]] = [
    {
        "slug": "uniprot",
        "adapter": "uniprot",
        "label": "UniProt",
        "family": "protein_annotation",
        "default_arguments": {"accession": "P04637", "retmax": 2, "timeout": 20},
        "required_input": "`--accession` or `--query`",
        "supports": "protein accession, reviewed/unreviewed status, sequence/function annotation provenance",
        "cannot_support": "new function, mechanism, causality, or clinical utility without primary evidence",
        "handoff": "Reef -> Iceberg/Anchor",
        "terms_url": "https://www.uniprot.org/help/license",
    },
    {
        "slug": "pubmed",
        "adapter": "pubmed",
        "label": "PubMed",
        "family": "literature_metadata",
        "default_arguments": {"query": "TP53", "retmax": 2, "timeout": 20},
        "required_input": "`--query`",
        "supports": "PubMed record discovery and PMID/query provenance",
        "cannot_support": "full-paper evidence, peer-review quality, mechanism, or clinical efficacy",
        "handoff": "Sounding/Reef -> Current/Iceberg",
        "terms_url": "https://www.ncbi.nlm.nih.gov/home/about/policies/",
    },
    {
        "slug": "europepmc",
        "adapter": "europepmc",
        "label": "Europe PMC",
        "family": "literature_metadata",
        "default_arguments": {"query": "TP53", "retmax": 2, "timeout": 20},
        "required_input": "`--query`",
        "supports": "literature metadata, abstract-level discovery, DOI/PMID/PMCID provenance",
        "cannot_support": "full methods/results quality or publication outcome unless inspected",
        "handoff": "Sounding/Reef -> Current/Iceberg",
        "terms_url": "https://europepmc.org/RestfulWebService",
    },
    {
        "slug": "chembl",
        "adapter": "chembl",
        "label": "ChEMBL",
        "family": "drug_target",
        "default_arguments": {"query": "aspirin", "retmax": 2, "timeout": 20},
        "required_input": "`--query`",
        "supports": "compound/target/assay metadata and ChEMBL identifier provenance",
        "cannot_support": "therapeutic efficacy, safety, mechanism, or clinical readiness",
        "handoff": "Reef -> Iceberg/Compass",
        "terms_url": "https://chembl.gitbook.io/chembl-interface-documentation/about",
    },
    {
        "slug": "opentargets",
        "adapter": "opentargets",
        "label": "Open Targets",
        "family": "drug_target",
        "default_arguments": {"ensembl_id": "ENSG00000141510", "retmax": 2, "timeout": 20},
        "required_input": "`--ensembl-id`",
        "supports": "target metadata and target-resource provenance",
        "cannot_support": "mechanism, therapeutic efficacy, or clinical readiness from association scores",
        "handoff": "Reef -> Iceberg/Compass",
        "terms_url": "https://platform-docs.opentargets.org/data-access",
    },
    {
        "slug": "string",
        "adapter": "string",
        "label": "STRING",
        "family": "protein_interaction",
        "default_arguments": {"identifier": "TP53", "species": 9606, "retmax": 2, "timeout": 20},
        "required_input": "`--identifier` or `--query`, plus explicit `--species`",
        "supports": "identifier mapping and protein association-resource provenance",
        "cannot_support": "direct physical binding, mechanism, causality, or disease relevance",
        "handoff": "Reef -> Iceberg/Compass",
        "terms_url": "https://string-db.org/cgi/access",
    },
    {
        "slug": "reactome",
        "adapter": "reactome",
        "label": "Reactome",
        "family": "pathway",
        "default_arguments": {"query": "TP53", "species_name": "Homo sapiens", "retmax": 2, "timeout": 20},
        "required_input": "`--query`",
        "supports": "pathway/resource discovery and pathway-context provenance",
        "cannot_support": "pathway activity, causal disease mechanism, or treatment effect",
        "handoff": "Reef -> Iceberg/Compass",
        "terms_url": "https://reactome.org/license",
    },
    {
        "slug": "quickgo",
        "adapter": "quickgo",
        "label": "QuickGO",
        "family": "ontology",
        "default_arguments": {"query": "apoptosis", "retmax": 2, "timeout": 20},
        "required_input": "`--query`",
        "supports": "GO term metadata and annotation-resource provenance",
        "cannot_support": "direct molecular mechanism, causality, or phenotype proof",
        "handoff": "Reef -> Iceberg/Harbor",
        "terms_url": "https://www.ebi.ac.uk/QuickGO/api/index.html",
    },
    {
        "slug": "clinvar",
        "adapter": "clinvar",
        "label": "ClinVar",
        "family": "variant_clinical_annotation",
        "default_arguments": {"query": "BRCA1", "retmax": 2, "timeout": 20},
        "required_input": "`--query`",
        "supports": "ClinVar record discovery and clinical-assertion metadata provenance",
        "cannot_support": "diagnosis, treatment guidance, or pathogenicity without inspected details",
        "handoff": "Reef -> Iceberg/Anchor",
        "terms_url": "https://www.ncbi.nlm.nih.gov/clinvar/",
    },
    {
        "slug": "gnomad",
        "adapter": "gnomad",
        "label": "gnomAD",
        "family": "population_genetics",
        "default_arguments": {"variant_id": "11-5227002-T-A", "gnomad_dataset": "gnomad_r4", "retmax": 2, "timeout": 20},
        "required_input": "`--variant-id`",
        "supports": "population-frequency or constraint-resource provenance",
        "cannot_support": "pathogenicity, diagnosis, treatment actionability, or mechanism",
        "handoff": "Reef -> Iceberg/Anchor",
        "terms_url": "https://gnomad.broadinstitute.org/help/terms",
    },
    {
        "slug": "alphafold_db",
        "adapter": "alphafold-db",
        "label": "AlphaFold DB",
        "family": "structure_modeling",
        "default_arguments": {"accession": "P04637", "retmax": 2, "timeout": 20},
        "required_input": "`--accession` or `--query`",
        "supports": "predicted-structure metadata provenance by UniProt accession",
        "cannot_support": "experimental structure proof, binding, druggability, or function",
        "handoff": "Reef -> Iceberg/Anchor",
        "terms_url": "https://alphafold.ebi.ac.uk/api-docs",
    },
    {
        "slug": "clinicaltrials",
        "adapter": "clinicaltrials",
        "label": "ClinicalTrials.gov",
        "family": "clinical_registry",
        "default_arguments": {"query": "melanoma", "retmax": 2, "timeout": 20},
        "required_input": "`--query`",
        "supports": "trial registration, status, design, and registry-field provenance",
        "cannot_support": "treatment efficacy, safety superiority, or clinical guidance",
        "handoff": "Reef -> Iceberg/Anchor/Compass",
        "terms_url": "https://clinicaltrials.gov/data-api/about-api",
    },
    {
        "slug": "ncbi_eutils",
        "adapter": "ncbi-eutils",
        "label": "NCBI E-utilities",
        "family": "entrez_metadata",
        "default_arguments": {"database": "gene", "query": "TP53", "retmax": 2, "timeout": 20},
        "required_input": "`--database` and `--query`",
        "supports": "Entrez record discovery and public metadata retrieval planning",
        "cannot_support": "full evidence, mechanism, causality, or absence-of-evidence claims",
        "handoff": "Reef -> Sounding/Iceberg/Harbor",
        "terms_url": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
    },
]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def query_script() -> str:
    return dedent(
        '''\
        #!/usr/bin/env python3
        """Per-database OCEAN Reef query-packet entrypoint.

        Generated file. Keep adapter-specific settings in ../adapter_config.json.
        """

        from __future__ import annotations

        from pathlib import Path
        import sys


        def _find_tools_root(start: Path) -> Path:
            for parent in [start, *start.parents]:
                candidate = parent / "common" / "database_adapter_entrypoint.py"
                if candidate.exists():
                    return parent
            raise RuntimeError("Could not find scripts/tools/common/database_adapter_entrypoint.py")


        TOOLS_ROOT = _find_tools_root(Path(__file__).resolve())
        sys.path.insert(0, str(TOOLS_ROOT / "common"))

        from database_adapter_entrypoint import main_for_adapter  # noqa: E402


        if __name__ == "__main__":
            raise SystemExit(main_for_adapter(Path(__file__).resolve().parents[1]))
        '''
    )


def readme_text(item: dict[str, Any]) -> str:
    example_args = " ".join(
        f"--{key.replace('_', '-')} {json.dumps(value)}"
        for key, value in item["default_arguments"].items()
        if key not in {"retmax", "timeout"}
    )
    return dedent(
        f"""\
        # {item['label']}

        OCEAN database adapter folder for `{item['adapter']}`.

        ## Scope

        - Family: `{item['family']}`
        - Required input: {item['required_input']}
        - Shared runner: `../../../run_reef_api_adapter.py`
        - Entry point: `scripts/query_packet.py`

        ## What This Adapter Does

        - Creates a bounded Reef API/database packet.
        - Records query target, official resource family, inspected fields, and evidence boundary.
        - Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

        ## Evidence Boundary

        This adapter can support: {item['supports']}.

        It cannot by itself support: {item['cannot_support']}.

        ## Example

        Dry-run query packet:

        ```bash
        python3 scripts/query_packet.py {example_args} \\
          --out outputs/{item['slug']}-reef-packet.json
        ```

        Bounded live query packet:

        ```bash
        python3 scripts/query_packet.py {example_args} \\
          --execute \\
          --out outputs/{item['slug']}-reef-packet.json
        ```

        ## Terms Boundary

        Check the source terms before reuse: {item['terms_url']}

        ## OCEAN Handoff

        {item['handoff']}. Do not treat database presence as primary experimental validation.
        """
    )


def api_json(item: dict[str, Any]) -> dict[str, Any]:
    default_args = item["default_arguments"]
    argv = ["python3", "scripts/query_packet.py"]
    for key, value in default_args.items():
        if key in {"retmax", "timeout"}:
            continue
        argv.extend([f"--{key.replace('_', '-')}", str(value)])
    argv.extend(["--retmax", str(default_args.get("retmax", 2)), "--out", f"outputs/{item['slug']}-reef-packet.json"])
    live_argv = [*argv[:-2], "--execute", *argv[-2:]]
    return {
        "schema_version": "ocean-database-tool-api-v1",
        "adapter": item["adapter"],
        "tool_name": item["label"],
        "tool_slug": item["slug"],
        "tool_family": item["family"],
        "interface_type": "reef_api_database_packet",
        "python_wrapper": "scripts/query_packet.py",
        "example_input": "examples/query.example.json",
        "default_output": f"outputs/{item['slug']}-reef-packet.json",
        "commands": [
            {
                "name": "query-packet",
                "description": "Create a bounded dry-run Reef API/database packet.",
                "argv": argv,
            },
            {
                "name": "query-packet-live",
                "description": "Create a bounded live Reef API/database packet with explicit network execution.",
                "argv": live_argv,
            },
        ],
        "output_contract": {
            "ocean_module": "Reef",
            "boundary_required": True,
            "handoff": item["handoff"],
        },
        "evidence_boundary": {
            "can_support": item["supports"],
            "cannot_support_alone": item["cannot_support"],
            "terms_url": item["terms_url"],
        },
    }


def tool_json(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": item["label"],
        "slug": item["slug"],
        "adapter": item["adapter"],
        "family": item["family"],
        "maturity": "L2 Reef API/database packet adapter",
        "required_input": item["required_input"],
        "evidence_level": "public API/database metadata only after query packet is inspected",
        "cannot_support_alone": [item["cannot_support"]],
        "handoff": item["handoff"],
    }


def adapter_config(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "ocean-database-adapter-config-v1",
        "adapter": item["adapter"],
        "slug": item["slug"],
        "label": item["label"],
        "family": item["family"],
        "default_arguments": item["default_arguments"],
        "required_input": item["required_input"],
        "can_support": item["supports"],
        "cannot_support": item["cannot_support"],
        "handoff": item["handoff"],
        "terms_url": item["terms_url"],
    }


def generate(base_dir: Path) -> list[str]:
    generated = []
    for item in DATABASES:
        tool_dir = base_dir / item["slug"]
        (tool_dir / "scripts").mkdir(parents=True, exist_ok=True)
        (tool_dir / "examples").mkdir(parents=True, exist_ok=True)
        (tool_dir / "outputs").mkdir(parents=True, exist_ok=True)
        write_json(tool_dir / "adapter_config.json", adapter_config(item))
        write_json(tool_dir / "api.json", api_json(item))
        write_json(tool_dir / "tool.json", tool_json(item))
        write_json(tool_dir / "examples" / "query.example.json", item["default_arguments"])
        (tool_dir / "README.md").write_text(readme_text(item), encoding="utf-8")
        script_path = tool_dir / "scripts" / "query_packet.py"
        script_path.write_text(query_script(), encoding="utf-8")
        script_path.chmod(0o755)
        generated.append(item["slug"])
    return generated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate OCEAN database adapter folders.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    base_dir = args.skill_dir / "scripts" / "tools" / "databases"
    generated = generate(base_dir)
    print(json.dumps({"generated": len(generated), "base_dir": str(base_dir), "slugs": generated}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
