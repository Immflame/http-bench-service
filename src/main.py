import argparse


async def parse_args():
    parser = argparse.ArgumentParser(prog='http-bench-service',
                                     description='Тестирование доступности HTTP-серверов',
                                     epilog="Пример: python bench.py -H https://ya.ru -C 5"
                                     )
    parser.add_argument('-C', '--count', type=int, help='Количество запросов', default=1)
    parser.add_argument('-O', '--output', type=argparse.FileType('w'), help='Файл для сохранения результптов')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-H', '--hosts', type=str, help='Хосты через запятую')
    group.add_argument('-F', '--file', type=argparse.FileType('r'), help='Файл со списком хостов')

    args = parser.parse_args()


if __name__ == "__main__":
    parse_args()