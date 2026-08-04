import asyncio
import sys
from src.cli import parse_args
from src.service.service import BenchmarkService
from src.exceptions import HttpBenchBaseException


async def main():
    args = parse_args()
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


if __name__ == "__main__":
    asyncio.run(main())
