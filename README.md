# logscan

`logscan` — CLI-утилита на Python для анализа серверного лог-файла. Программа находит IPv4-адреса и SHA256-хэши с помощью регулярных выражений, проверяет их через VirusTotal API (либо использует mock без API-ключа) и сохраняет отчёт в CSV или JSON.

## Структура проекта

```text
logscan/
├── main.py
├── requirements.txt
├── README.md
├── logs/
│   └── sample.log
├── output/
│   └── report.csv
└── modules/
    ├── log_parser.py
    ├── virustotal.py
    └── report_generator.py
```

## Установка

Нужен Python 3.9 или новее. В терминале перейдите в папку `logscan` и установите зависимости:

```bash
python -m pip install -r requirements.txt
```

## Запуск

**CSV-отчёт без API-ключа (mock):**

```bash
python main.py -log-file logs/sample.log -output output/report.csv -format csv
```

**JSON-отчёт без API-ключа (mock):**

```bash
python main.py -log-file logs/sample.log -output output/report.json -format json
```

**Проверка через VirusTotal с API-ключом:**

```bash
python main.py -log-file logs/sample.log -api-key YOUR_API_KEY -output output/report.csv -format csv
```

Аргументы командной строки:

- `-log-file` — путь к файлу с логами (обязательный).
- `-api-key` — API-ключ VirusTotal (необязательный; без него включается mock).
- `-output` — путь к выходному файлу отчёта (обязательный).
- `-format` — формат отчёта: `csv` или `json` (обязательный).

## Что делает программа

1. Читает лог-файл, извлекает IPv4-адреса и SHA256-хэши с помощью `re`, проверяет корректность IPv4 и убирает повторы.
2. Если задан API-ключ, отправляет запросы на получение имеющихся отчётов VirusTotal: `GET /api/v3/ip_addresses/{ip}` для IP и `GET /api/v3/files/{hash}` для SHA256. Если ключ не задан, выполняет mock-проверку без сетевых запросов.
3. Для каждого артефакта формирует поля `value` (значение), `type` (`IP`/`HASH`), `result` (результат проверки) и `date` (дата и время проверки в UTC).
4. Записывает отчёт в указанный CSV- или JSON-файл. Сообщения о ходе работы, статусах и ошибках выводятся в терминал с помощью `logging`.

Результаты проверки:

- `MOCK: NOT_CHECKED` — mock: реальная проверка **не проводилась**.
- `MALICIOUS: N detections` — VirusTotal сообщил о N вредоносных срабатываниях.
- `SUSPICIOUS: N detections` — VirusTotal сообщил о N подозрительных срабатываниях (при отсутствии вредоносных).
- `NO_DETECTIONS` — по доступной статистике вредоносных и подозрительных срабатываний нет. Это не доказывает безопасность объекта.
- `NOT_FOUND` — объект не найден в VirusTotal (HTTP 404).
- `NO_DATA` — в ответе отсутствует статистика анализа.
- `ERROR` — ошибка запроса или разбора ответа (подробности выводятся в журнал терминала).

Пример входных данных: `logs/sample.log` — учебные записи с тестовыми IP-адресами и SHA256-хэшами. Пример выходных данных: `output/report.csv`, сформированный в mock-режиме.

Документация API VirusTotal:
- https://docs.virustotal.com/reference/ip-info
- https://docs.virustotal.com/reference/file-info

**Примечание:** запросы в VirusTotal могут передавать индикаторы во внешнюю службу. Не отправляйте конфиденциальные или персональные данные без разрешения.
