from argparse import ArgumentParser, ArgumentTypeError
from urllib.parse import urlparse
from importlib.metadata import version
import os
import logging

logger = logging.getLogger(__name__)

class Parser:
    def __init__(self):
        self.parser = ArgumentParser(
            prog='bench',
            usage='bench [-h] [-C COUNT] [-O OUTPUT] (-H HOSTS | -F FILE)',
            description='Тестирование доступности HTTP-серверов',
            epilog="Пример команды: bench -H https://ya.ru --count 5"
        )
        self.__add_arguments()

    def parse_args(self):
        return self.parser.parse_args()

    def __add_arguments(self):
        self.parser.add_argument(
            '-C', '--count',
            type=self.__validate_count,
            default=1,
            help='Количество запросов на каждый хост (по умолчанию 1)'
        )

        self.parser.add_argument(
            '-O', '--output',
            type=str,
            default=None,
            help='Файл для сохранения результатов'
        )

        required_group = self.parser.add_mutually_exclusive_group(required=True)
        required_group.add_argument(
            '-H', '--hosts',
            type=self.__validate_hosts,
            help='Хосты через запятую (например: https://ya.ru,https://google.com)'
        )

        required_group.add_argument(
            '-F', '--file',
            type=self.__validate_input_file,
            help='Файл со списком хостов (один на строку)'
        )

        config_group = self.parser.add_argument_group('Configuration')

        config_group.add_argument(
            '--max-keepalive-conn',
            type=int,
            default=20,
            help='Максимальное количество одновременных подключений (по умолчанию 20)'
        )

        config_group.add_argument(
            '--verbose',
            action='store_true',
            help='Включить подробный вывод (по умолчанию отключено)'
        )

        config_group.add_argument(
            '--timeout',
            type=float,
            default=3.0,
            help='Таймаут в секундах (по умолчанию 3.0)'
        )

        config_group.add_argument(
            '-V', '--version',
            action='version',
            version=f'%(prog)s {self.get_version()}',
            help='Версия программы'
        )

    @staticmethod
    def get_version() -> str:
        return version('http-bench-service')

    @staticmethod
    def __validate_hosts(value: str) -> list[str]:
        hosts = [h.strip() for h in value.split(',') if h.strip()]
        if not hosts:
            raise ArgumentTypeError("Список хостов не может быть пустым")
        for host in hosts:
            parsed = urlparse(host)
            if not (parsed.scheme in ('http', 'https') and parsed.netloc):
                raise ArgumentTypeError(f"Некорректный URL: {host}. Ожидается формат https://example.com")
        return hosts

    @staticmethod
    def __validate_input_file(value: str) -> str:
        if not os.path.isfile(value):
            raise ArgumentTypeError(f"Файл {value} не найден")
        if os.path.getsize(value) == 0:
            raise ArgumentTypeError(f"Файл {value} пуст")
        return value

    @staticmethod
    def __validate_count(value: str) -> int:
        try:
            count = int(value)
            if count < 1:
                raise ArgumentTypeError("Количество запросов должно быть >= 1")
            return count
        except ValueError:
            raise ArgumentTypeError("Количество запросов должно быть числом")
