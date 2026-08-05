import argparse
import sys
from src.service.service import BenchmarkService
from src.exceptions import HttpBenchBaseException
from src.utils.validators import validate_hosts_str, validate_count


async def cli():

    """ Парсит аргументы командной строки и запускает бенчмарки """

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
        type=validate_hosts_str,
        help='Хосты через запятую (например: https://ya.ru,https://google.com)'
    )

    group.add_argument(
        '-F', '--file',
        type=str,
        help='Файл со списком хостов (один на строку)'
    )

    args = parser.parse_args()

    service = BenchmarkService()
    try:
        await service.benchmark(
            hosts=args.hosts,
            count=args.count,
            input_file=args.file,
            output_file=args.output
        )
    except HttpBenchBaseException as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)
