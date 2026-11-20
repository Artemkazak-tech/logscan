import csv
import json
from pathlib import Path


REPORT_FIELDS = ["value", "type", "result", "date"]


def generate_report(report, output_file, report_format):
    """Сохраняет результаты проверки в CSV или JSON."""
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    if report_format == "csv":
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=REPORT_FIELDS)
            writer.writeheader()
            writer.writerows(report)
    elif report_format == "json":
        with path.open("w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=4)
    else:
        raise ValueError("Неподдерживаемый формат отчёта")
