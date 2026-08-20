import asyncio
from http_bench_service.http_client import AsyncHTTPClient
from http_bench_service.file_client import FileClient
from http_bench_service.exceptions import BenchmarkBaseException


class Benchmarker:
    def __init__(self,
                 http_client: AsyncHTTPClient,
                 io_client: FileClient):

        self.__http_client: AsyncHTTPClient = http_client
        self.__io_client: FileClient = io_client

    async def benchmark(
            self,
            hosts: list[str] | None = None,
            count: int = 1,
            input_file: str | None = None,
            output_file: str | None = None
    ):
        """ Запускает тестирование доступности хостов """
        target_hosts = hosts if hosts else self.__io_client.read_lines(input_file)
        if not target_hosts:
            raise BenchmarkBaseException("Список хостов пуст")

        async with self.__http_client as http_client:
            coroutines = []
            for host in target_hosts:
                for _ in range(count):
                    coroutines.append(http_client.get(host))

            results = {host: [] for host in target_hosts}
            for completed in asyncio.as_completed(coroutines): # Получает ответ от корутин по мере их выполнения
                response = await completed
                results[response['url']].append(response)

        output_text = self.__format_benchmark_report(results)

        if output_file:
            self.__io_client.write_lines(output_file, [output_text])
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

                if 'elapsed' in response and response['elapsed'] is not None:
                    times.append(response['elapsed'])

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
