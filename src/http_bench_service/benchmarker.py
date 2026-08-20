import asyncio
from http_bench_service.http_client import AsyncHTTPClient
from http_bench_service.file_client import FileClient


class Benchmarker:
    def __init__(self,
                 http_client: AsyncHTTPClient,
                 file_client: FileClient):
        self.__http_client: AsyncHTTPClient = http_client
        self.__file_client: FileClient = file_client

    async def benchmark(
            self,
            hosts: list[str] | None = None,
            input_file: str | None = None,
            count: int = 1,
            output_file: str | None = None
    ):
        hosts = hosts if hosts else self.__file_client.read_lines(input_file)
        async with self.__http_client as http_client:
            tasks = []
            for host in hosts:
                for _ in range(count):
                    tasks.append(http_client.get(host))

            results = {host: [] for host in hosts}
            responses = await asyncio.gather(*tasks)
            for res in responses:
                results[res['url']].append(res)

        output_text = self.__format_benchmark_report(results)

        if output_file:
            self.__file_client.write_lines(output_file, [output_text])
            print(f"Результаты сохранены в {output_file}")
        else:
            print(output_text)


    def __format_benchmark_report(self, raw_results: dict[str, list[dict]]) -> str:
        """ Возвращает строку со статистикой в читаемом формате """
        lines = ["*" * 60, "РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ", "*" * 60]

        for host, responses in raw_results.items():
            stats = self.__collect_statistics(responses)
            lines.append(f"\nHost: {host}")
            lines.append(f"  Success: {stats['success']}")
            lines.append(f"  Failed: {stats['failed']}")
            lines.append(f"  Errors: {stats['errors']}")
            lines.append(f"  Min: {stats['min'] * 1000:.2f} ms")
            lines.append(f"  Max: {stats['max'] * 1000:.2f} ms")
            lines.append(f"  Avg: {stats['avg'] * 1000:.2f} ms")
            lines.append("-" * 40)

        return '\n'.join(lines)

    def __collect_statistics(self, responses: list[dict]) -> dict:
        """ Считает общую статистику по каждому хосту"""
        success = 0
        failed = 0
        errors = 0
        times = []

        for response in responses:
            if 'error' in response:
                errors += 1

            elif 'status_code' in response:
                if 200 <= response['status_code'] < 400:
                    success += 1
                else:
                    failed += 1

                if 'time_duration' in response and response['time_duration'] is not None:
                    times.append(response['time_duration'])

        min_time = min(times) if times else 0.0
        max_time = max(times) if times else 0.0
        avg_time = sum(times) / len(times) if times else 0.0

        return {
            'success': success,
            'failed': failed,
            'errors': errors,
            'min': min_time,
            'max': max_time,
            'avg': avg_time
        }
