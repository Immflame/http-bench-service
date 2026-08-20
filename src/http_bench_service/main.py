import asyncio
import logging
import sys
from argparse import ArgumentTypeError
from http_bench_service.benchmarker import Benchmarker
from http_bench_service.exceptions import BenchmarkBaseException
from http_bench_service.parser import Parser
from http_bench_service.http_client import AsyncHTTPClient
from http_bench_service.file_client import FileClient
from time import perf_counter

logger = logging.getLogger(__name__)

def setup_logging(verbose: bool = False):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

async def main():
    prog_start = perf_counter()
    parser = Parser()
    try:
        args = parser.parse_args()
    except ArgumentTypeError as e:
        logger.error("%s", e)
        sys.exit(1)
    setup_logging(verbose=args.verbose)
    file_client = FileClient()
    http_client = AsyncHTTPClient(
        timeout=args.timeout,
        max_concurrent_tasks=100,
        max_keepalive_connections=args.max_keepalive_connections
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
        logger.exception("Ошибка: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.exception("Неожиданная ошибка: %s", e)
        sys.exit(1)
    finally:
        finish = perf_counter() - prog_start
        logging.info(f"Общее время выполнения - {finish} s")


def entrypoint():
    asyncio.run(main())


if __name__ == "__main__":
    entrypoint()
