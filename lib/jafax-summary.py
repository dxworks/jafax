#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from summary_render import render_summary


SUMMARY_DATA_FILE_NAME = 'jafax-summary-data.json'


def build_payload(summary_data: dict[str, Any]) -> dict[str, Any]:
    status = str(summary_data.get('status') or 'success')
    generated_at = _format_generated_at(summary_data.get('generatedAt'))
    layout_objects_count = _to_int(summary_data.get('layoutObjectsCount'))
    files_count = _to_int(summary_data.get('filesCount'))
    top_level_classes_count = _to_int(summary_data.get('topLevelClassesCount'))
    internal_relations_count = _to_int(summary_data.get('internalRelationsCount'))
    external_relations_count = _to_int(summary_data.get('externalRelationsCount'))
    metrics_count = _to_int(summary_data.get('metricsCount'))
    imports_count = _to_int(summary_data.get('importsCount'))
    interfaces_count = _to_int(summary_data.get('interfacesCount'))
    abstract_classes_count = _to_int(summary_data.get('abstractClassesCount'))

    metadata = {
        'project.name': summary_data.get('projectName', 'unknown'),
        'layout.only': str(bool(summary_data.get('onlyLayout'))).lower(),
        'layout.objects': layout_objects_count,
        'files.total': files_count,
        'classes.top.level': top_level_classes_count,
        'relations.internal': internal_relations_count,
        'relations.external': external_relations_count,
        'metrics.rows': metrics_count,
        'imports.rows': imports_count,
        'interfaces.count': interfaces_count,
        'abstract.classes.count': abstract_classes_count,
        'generated.at': generated_at,
    }

    markdown = '\n'.join(
        [
            '## JaFaX',
            '',
            f"- Project: {summary_data.get('projectName', 'unknown')}",
            f"- Layout only mode: {str(bool(summary_data.get('onlyLayout'))).lower()}",
            f"- Layout objects: {_format_int(layout_objects_count)}",
            f"- Source files: {_format_int(files_count)}",
            f"- Top-level classes: {_format_int(top_level_classes_count)}",
            f"- Internal relations: {_format_int(internal_relations_count)}",
            f"- External relations: {_format_int(external_relations_count)}",
            f"- Metrics rows: {_format_int(metrics_count)}",
            f"- Imports rows: {_format_int(imports_count)}",
            f"- Interfaces: {_format_int(interfaces_count)}",
            f"- Abstract classes: {_format_int(abstract_classes_count)}",
            f'- Generated at: {generated_at}',
        ]
    )

    template_model = {
        'projectName': summary_data.get('projectName', 'unknown'),
        'onlyLayout': str(bool(summary_data.get('onlyLayout'))).lower(),
        'layoutObjectsCountFormatted': _format_int(layout_objects_count),
        'filesCountFormatted': _format_int(files_count),
        'topLevelClassesCountFormatted': _format_int(top_level_classes_count),
        'internalRelationsCountFormatted': _format_int(internal_relations_count),
        'externalRelationsCountFormatted': _format_int(external_relations_count),
        'metricsCountFormatted': _format_int(metrics_count),
        'importsCountFormatted': _format_int(imports_count),
        'interfacesCountFormatted': _format_int(interfaces_count),
        'abstractClassesCountFormatted': _format_int(abstract_classes_count),
        'generatedAt': generated_at,
    }

    return {
        'tool': 'jafax',
        'status': status,
        'metadata': metadata,
        'markdown': markdown,
        'templateModel': template_model,
    }


def build_missing_payload() -> dict[str, Any]:
    return {
        'tool': 'jafax',
        'status': 'missing',
        'metadata': {},
        'markdown': '\n'.join([
            '## JaFaX',
            '',
            '- Summary input is missing',
        ]),
        'templateModel': {
            'isMissing': True,
        },
    }


def _to_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def _format_int(value: int) -> str:
    return f'{value:,}'


def _format_generated_at(value: Any) -> str:
    if value is None:
        return 'unknown'

    raw_value = str(value).strip()
    if not raw_value:
        return 'unknown'

    try:
        parsed = datetime.fromisoformat(raw_value.replace('Z', '+00:00'))
    except ValueError:
        return raw_value

    return parsed.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


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
            print(
                f"summary input missing for jafax: expected '{SUMMARY_DATA_FILE_NAME}' in "
                f"'{target_directory}'; generating missing summary artifacts"
            )
            payload = build_missing_payload()
        else:
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
