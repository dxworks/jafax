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
    source_lines_count = _to_int(_get_value(summary_data, 'sourceLines', 'sourceLinesCount', 'sourceCodeLines'))
    layout_objects_count = _to_int(summary_data.get('layoutObjectsCount'))
    files_count = _to_int(summary_data.get('filesCount'))
    top_level_classes_count = _to_int(summary_data.get('topLevelClassesCount'))

    metadata = {
        'source.lines.total': source_lines_count,
        'files.total': files_count,
        'layout.objects': layout_objects_count,
        'classes.top.level': top_level_classes_count,
    }

    markdown = '\n'.join(
        [
            '## JaFaX',
            '',
            f"- Source lines: {_format_int(source_lines_count)} / Source files: {_format_int(files_count)}",
            f"- Layout objects: {_format_int(layout_objects_count)}",
            f"- Top-level classes: {_format_int(top_level_classes_count)}",
        ]
    )

    template_model = {
        'sourceLinesCountFormatted': _format_int(source_lines_count),
        'filesCountFormatted': _format_int(files_count),
        'layoutObjectsCountFormatted': _format_int(layout_objects_count),
        'topLevelClassesCountFormatted': _format_int(top_level_classes_count),
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


def _get_value(summary_data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in summary_data:
            return summary_data[key]

    return default


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
        try:
            parsed = datetime.strptime(raw_value, '%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc)
        except ValueError:
            return raw_value

    return _format_local_datetime(parsed)


def _format_local_datetime(value: datetime) -> str:
    local_value = value.astimezone()
    return f"{local_value.strftime('%Y-%m-%d %H:%M:%S')} {_format_gmt_offset(local_value.strftime('%z'))}"


def _format_gmt_offset(offset: str) -> str:
    if len(offset) != 5:
        return 'GMT+0'

    sign = offset[0]
    hours = int(offset[1:3])
    minutes = int(offset[3:5])

    if minutes == 0:
        return f'GMT{sign}{hours}'

    return f'GMT{sign}{hours}:{minutes:02d}'


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
