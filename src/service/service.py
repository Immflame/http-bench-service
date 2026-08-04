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

        tasks = []
        task_to_host = []
        for host in target_hosts:
            for _ in range(count):
                task = self._http_client.get(host)
                tasks.append(task)
                task_to_host.append(host)

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        host_responses = {}
        for host, response in zip(task_to_host, responses):
            if host not in host_responses:
                host_responses[host] = []

            if isinstance(response, Exception):
                host_responses[host].append({'url': host, 'error': str(response)})
            else:
                host_responses[host].append(response)

        unique_hosts = list(dict.fromkeys(target_hosts))
        results = {}
        for host in unique_hosts:
            stats = collect_statistics(host_responses[host])
            results[host] = stats

        output_text = self._format_results(results)

        if output_file:
            self._io_client.write_lines(output_file, [output_text])
            print(f"Результаты сохранены в {output_file}")
        else:
            print(output_text)

        await self._http_client.close()

    @staticmethod
    def _format_results(results: dict) -> str:
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
