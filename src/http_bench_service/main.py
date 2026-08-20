import asyncio
import sys
from argparse import ArgumentTypeError
from http_bench_service.benchmarker import Benchmarker
from http_bench_service.exceptions import BenchmarkBaseException
from http_bench_service.parser import Parser
from http_bench_service.http_client import AsyncHTTPClient
from http_bench_service.file_client import FileClient


async def main():
    parser = Parser()
    try:
        args = parser.parse_args()
    except ArgumentTypeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    http_client = AsyncHTTPClient()
    file_client = FileClient()
    service = Benchmarker(http_client, file_client)
    try:
        await service.benchmark(
            hosts=args.hosts,
            count=args.count,
            input_file=args.file,
            output_file=args.output
        )
    except BenchmarkBaseException as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def entrypoint():
    asyncio.run(main())


if __name__ == "__main__":
    entrypoint()
