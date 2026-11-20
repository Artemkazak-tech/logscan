import argparse
import logging
from datetime import datetime, timezone

from modules.log_parser import extract_artifacts
from modules.virustotal import check_artifact
from modules.report_generator import generate_report


def main():
    parser = argparse.ArgumentParser(
        prog="logscan",
        description="Анализ лог-файла и проверка IP-адресов и SHA256-хэшей через VirusTotal.",
    )
    parser.add_argument("-log-file", required=True, help="Путь к лог-файлу")
    parser.add_argument("-api-key", help="Ключ VirusTotal (без ключа используется mock)")
    parser.add_argument("-output", required=True, help="Путь к файлу отчёта")
    parser.add_argument("-format", choices=["csv", "json"], required=True, help="Формат отчёта")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    logging.info("Начало анализа: %s", args.log_file)
    try:
        artifacts = extract_artifacts(args.log_file)
    except OSError as error:
        logging.error("Не удалось прочитать лог-файл: %s", error)
        return 1

    logging.info("Найдено уникальных артефактов: %s", len(artifacts))
    if not args.api_key:
        logging.info("Ключ VirusTotal не задан: используется mock")

    report = []
    for artifact in artifacts:
        result = check_artifact(artifact["value"], artifact["type"], args.api_key)
        logging.info("Проверка %s %s: %s", artifact["type"], artifact["value"], result)
        report.append(
            {
                "value": artifact["value"],
                "type": artifact["type"],
                "result": result,
                "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
        )

    try:
        generate_report(report, args.output, args.format)
    except OSError as error:
        logging.error("Не удалось записать отчёт: %s", error)
        return 1

    logging.info("Отчёт сохранён: %s", args.output)
    logging.info("Анализ завершён")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
