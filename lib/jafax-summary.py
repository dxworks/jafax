#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from summary_render import render_summary


SUMMARY_DATA_FILE_NAME = 'jafax-summary-data.json'


def build_payload(summary_data: dict[str, Any]) -> dict[str, Any]:
    status = str(summary_data.get('status') or 'success')

    metadata = {
        'project.name': summary_data.get('projectName', 'unknown'),
        'layout.only': str(bool(summary_data.get('onlyLayout'))).lower(),
        'layout.objects': _to_int(summary_data.get('layoutObjectsCount')),
        'files.total': _to_int(summary_data.get('filesCount')),
        'classes.top.level': _to_int(summary_data.get('topLevelClassesCount')),
        'relations.internal': _to_int(summary_data.get('internalRelationsCount')),
        'relations.external': _to_int(summary_data.get('externalRelationsCount')),
        'metrics.rows': _to_int(summary_data.get('metricsCount')),
        'imports.rows': _to_int(summary_data.get('importsCount')),
        'interfaces.count': _to_int(summary_data.get('interfacesCount')),
        'abstract.classes.count': _to_int(summary_data.get('abstractClassesCount')),
        'generated.at': summary_data.get('generatedAt', 'unknown'),
    }

    markdown = '\n'.join(
        [
            '## JaFaX',
            '',
            f'- Status: {status}',
            f"- Project: {summary_data.get('projectName', 'unknown')}",
            f"- Layout only mode: {str(bool(summary_data.get('onlyLayout'))).lower()}",
            f"- Layout objects: {_to_int(summary_data.get('layoutObjectsCount'))}",
            f"- Source files: {_to_int(summary_data.get('filesCount'))}",
            f"- Top-level classes: {_to_int(summary_data.get('topLevelClassesCount'))}",
            f"- Internal relations: {_to_int(summary_data.get('internalRelationsCount'))}",
            f"- External relations: {_to_int(summary_data.get('externalRelationsCount'))}",
            f"- Metrics rows: {_to_int(summary_data.get('metricsCount'))}",
            f"- Imports rows: {_to_int(summary_data.get('importsCount'))}",
            f"- Interfaces: {_to_int(summary_data.get('interfacesCount'))}",
            f"- Abstract classes: {_to_int(summary_data.get('abstractClassesCount'))}",
            f"- Generated at: {summary_data.get('generatedAt', 'unknown')}",
        ]
    )

    template_model = {
        'status': status,
        'statusClass': _to_status_class(status),
        'projectName': summary_data.get('projectName', 'unknown'),
        'onlyLayout': str(bool(summary_data.get('onlyLayout'))).lower(),
        'layoutObjectsCount': _to_int(summary_data.get('layoutObjectsCount')),
        'filesCount': _to_int(summary_data.get('filesCount')),
        'topLevelClassesCount': _to_int(summary_data.get('topLevelClassesCount')),
        'internalRelationsCount': _to_int(summary_data.get('internalRelationsCount')),
        'externalRelationsCount': _to_int(summary_data.get('externalRelationsCount')),
        'metricsCount': _to_int(summary_data.get('metricsCount')),
        'importsCount': _to_int(summary_data.get('importsCount')),
        'interfacesCount': _to_int(summary_data.get('interfacesCount')),
        'abstractClassesCount': _to_int(summary_data.get('abstractClassesCount')),
        'generatedAt': summary_data.get('generatedAt', 'unknown'),
    }

    return {
        'tool': 'jafax',
        'status': status,
        'metadata': metadata,
        'markdown': markdown,
        'templateModel': template_model,
    }


def _to_status_class(status: str) -> str:
    if status == 'success':
        return 'status-success'
    if status == 'partial':
        return 'status-warning'
    if status == 'failed':
        return 'status-error'
    return 'status-unknown'


def _to_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog='jafax-summary.py',
        description='Generates JaFaX summary artifacts for Voyager',
    )
    parser.add_argument('results_directory', nargs='?', default='results')
    args = parser.parse_args()

    target_directory = Path(args.results_directory).resolve()
    summary_data_path = target_directory / SUMMARY_DATA_FILE_NAME

    try:
        if not summary_data_path.exists():
            raise FileNotFoundError(f'missing {SUMMARY_DATA_FILE_NAME}. Run JaFaX extraction before summary')

        payload = build_payload(json.loads(summary_data_path.read_text(encoding='utf-8')))
        rendered = render_summary(target_directory, payload)
        print(f"Generated summary markdown at {rendered['summaryMdPath']}")
        print(f"Generated summary html at {rendered['summaryHtmlPath']}")
        return 0
    except Exception as error:
        print(f"summary generation failed for '{target_directory}': {error}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
