import asyncio
import sys
from argparse import ArgumentTypeError
from http_bench_service.benchmarker import Benchmarker
from http_bench_service.exceptions import BenchmarkBaseException
from http_bench_service.parser import Parser
from http_bench_service.http_client import AsyncHTTPClient
from http_bench_service.file_client import FileClient
from time import perf_counter


async def main():
    prog_start = perf_counter()
    parser = Parser()
    try:
        args = parser.parse_args()
    except ArgumentTypeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    file_client = FileClient()
    http_client = AsyncHTTPClient(
        timeout=2.0,
        max_concurrent_tasks=100,
        max_keepalive_connections=30
    )
    bench = Benchmarker(http_client=http_client, file_client=file_client)
    try:
        await bench.benchmark(
            hosts=args.hosts,
            input_file=args.file,
            count=args.count,
            output_file=args.output
        )
    except BenchmarkBaseException as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        print(f"Общее время выполнения: {perf_counter() - prog_start}")


def entrypoint():
    asyncio.run(main())


if __name__ == "__main__":
    entrypoint()
