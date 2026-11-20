import logging

import requests


API_URL = "https://www.virustotal.com/api/v3"


def check_artifact(value, artifact_type, api_key=None):
    """Возвращает результат проверки IP или SHA256 в VirusTotal либо mock."""
    if not api_key:
        return "MOCK: NOT_CHECKED"

    if artifact_type == "IP":
        endpoint = "ip_addresses"
    else:
        endpoint = "files"

    url = f"{API_URL}/{endpoint}/{value}"
    headers = {"x-apikey": api_key, "accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 404:
            return "NOT_FOUND"
        response.raise_for_status()
        data = response.json()
        stats = data["data"]["attributes"].get("last_analysis_stats")
        if not isinstance(stats, dict):
            return "NO_DATA"

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        if malicious > 0:
            return f"MALICIOUS: {malicious} detections"
        if suspicious > 0:
            return f"SUSPICIOUS: {suspicious} detections"
        return "NO_DETECTIONS"

    except (requests.RequestException, ValueError, KeyError, TypeError) as error:
        logging.error("Ошибка запроса VirusTotal для %s: %s", value, error)
        return "ERROR"
