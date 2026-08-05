from urllib.parse import urlparse
from src.exceptions import HttpBenchBaseException


def validate_hosts_list(hosts: list[str]) -> list[str]:
    """Проверяет каждый URL в списке на корректность схемы и netloc"""
    for host in hosts:
        parsed = urlparse(host)
        if not (parsed.scheme in ('http', 'https') and parsed.netloc):
            raise HttpBenchBaseException(
                f"Некорректный URL: {host}. Ожидается формат https://example.com"
            )
    return hosts


def validate_hosts_str(value: str) -> list[str]:
    """Разбивает строку с хостами (через запятую) и валидирует каждый"""
    hosts = [h.strip() for h in value.split(',') if h.strip()]
    return validate_hosts_list(hosts)


def validate_count(value: str) -> int:
    """Проверяет, что значение — целое число >= 1"""
    try:
        count = int(value)
        if count < 1:
            raise HttpBenchBaseException("Количество запросов должно быть >= 1")
        return count
    except ValueError:
        raise HttpBenchBaseException("Количество запросов должно быть числом")
