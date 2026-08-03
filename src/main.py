import argparse
from src.service import BenchmarkService


def main():
    args = parse_args()
    benchmark = BenchmarkService()

    try:
        results = benchmark.start_test(
            hosts=args.hosts.split(',') if args.hosts else None,
            count_requests=args.count,
            input_file=args.file,
            output_file=args.output
        )

        # if not args.output:
        #     benchmark.print_results(results)

    except Exception as e:
        print(f"❌ Ошибка: {e}")


def parse_args():
    parser = argparse.ArgumentParser(prog='http-bench-service',
                                     description='Тестирование доступности HTTP-серверов',
                                     epilog="Пример: python bench.py -H https://ya.ru -C 5"
                                     )
    parser.add_argument('-C', '--count', type=int, help='Количество запросов', default=1)
    parser.add_argument('-O', '--output', type=str, help='Файл для сохранения результптов')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-H', '--hosts', type=str, help='Хосты через запятую')
    group.add_argument('-F', '--file', type=str, help='Файл со списком хостов')

    return parser.parse_args()


if __name__ == "__main__":
    main()