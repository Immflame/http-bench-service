import argparse
from urllib.parse import urlparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog='http-bench-service',
        description='Тестирование доступности HTTP-серверов',
        epilog="Пример: python bench.py -H https://ya.ru -C 5"
    )

    parser.add_argument(
        '-C', '--count',
        type=validate_count,
        default=1,
        help='Количество запросов на каждый хост (по умолчанию 1)'
    )

    parser.add_argument(
        '-O', '--output',
        type=str,
        default=None,
        help='Файл для сохранения результатов'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-H', '--hosts',
        type=validate_hosts,
        help='Хосты через запятую (например: https://ya.ru,https://google.com)'
    )

    group.add_argument(
        '-F', '--file',
        type=str,
        help='Файл со списком хостов (один на строку)'
    )

    return parser.parse_args()


def validate_count(value: str):
    try:
        count = int(value)
        if count < 1:
            raise argparse.ArgumentTypeError("Количество запросов должно быть >= 1")
        return count
    except ValueError:
        raise argparse.ArgumentTypeError("Количество запросов должно быть числом")


def validate_hosts(value: str):
    hosts = [h.strip() for h in value.split(',') if h.strip()]
    for host in hosts:
        parsed = urlparse(host)
        if not (parsed.scheme in ('http', 'https') and parsed.netloc):
            raise argparse.ArgumentTypeError(
                f"Некорректный URL: {host}. Ожидается формат https://example.com"
            )
    return hosts
