import ipaddress
import re


ARTIFACT_PATTERN = re.compile(
    r"(?P<HASH>(?<![A-Za-z0-9])[a-fA-F0-9]{64}(?![A-Za-z0-9]))"
    r"|(?P<IP>(?<![A-Za-z0-9.])(?:\d{1,3}\.){3}\d{1,3}(?![A-Za-z0-9.]))"
)


def extract_artifacts(log_file):
    """Извлекает уникальные IPv4-адреса и SHA256-хэши из лог-файла."""
    artifacts = []
    seen = set()

    with open(log_file, "r", encoding="utf-8") as file:
        for line in file:
            for match in ARTIFACT_PATTERN.finditer(line):
                if match.group("IP"):
                    value = match.group("IP")
                    try:
                        ipaddress.IPv4Address(value)
                    except ipaddress.AddressValueError:
                        continue
                    artifact_type = "IP"
                else:
                    value = match.group("HASH").lower()
                    artifact_type = "HASH"

                unique_id = (artifact_type, value)
                if unique_id not in seen:
                    seen.add(unique_id)
                    artifacts.append({"value": value, "type": artifact_type})

    return artifacts
