import asyncio
from src.client import HTTPClient, FileIOClient
from src.utils import collect_statistics
from src.exceptions import HttpBenchBaseException


class BenchmarkService:
    def __init__(self):
        self._http_client = HTTPClient()
        self._io_client = FileIOClient()

    async def benchmark(
        self,
        hosts: list[str] | None = None,
        count: int = 1,
        input_file: str | None = None,
        output_file: str | None = None
    ):
        if hosts and input_file:
            raise HttpBenchBaseException("Нельзя одновременно указывать -H и -F")

        target_hosts = hosts if hosts else self._io_client.read_lines(input_file)
        if not target_hosts:
            raise HttpBenchBaseException("Список хостов пуст")

        results = {}
        for host in target_hosts:
            tasks = [self._http_client.get(host) for _ in range(count)]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            processed = []
            for res in responses:
                if isinstance(res, Exception):
                    processed.append({'url': host, 'error': str(res)})
                else:
                    processed.append(res)
            stats = collect_statistics(processed)
            results[host] = stats

        output_text = self._format_results(results)
        if output_file:
            self._io_client.write_lines(output_file, [output_text])
            print(f"Результаты сохранены в {output_file}")
        else:
            print(output_text)

        await self._http_client.close()

    def _format_results(self, results: dict) -> str:
        lines = []
        lines.append("*" * 60)
        lines.append("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        lines.append("*" * 60)
        for host, stats in results.items():
            lines.append(f"\nHost: {host}")
            lines.append(f"  Success: {stats['success']}")
            lines.append(f"  Failed: {stats['failed']}")
            lines.append(f"  Errors: {stats['errors']}")
            lines.append(f"  Min: {stats['min'] * 1000:.2f} ms")
            lines.append(f"  Max: {stats['max'] * 1000:.2f} ms")
            lines.append(f"  Avg: {stats['avg'] * 1000:.2f} ms")
            lines.append("-" * 40)
        return '\n'.join(lines)
