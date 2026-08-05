import asyncio
from src.client import AsyncHTTPClient, FileIOClient
from src.utils.report import format_benchmark_report
from src.exceptions import HttpBenchBaseException
from src.utils.validators import validate_hosts_list


class BenchmarkService:
    """
    Сервис для проведения HTTP-бенчмарка

    Attributes:
        _http_client (AsyncHTTPClient): HTTP-клиент
        _io_client (FileIOClient): Клиент для чтения и записи файлов
    """
    def __init__(self):
        self._http_client = AsyncHTTPClient()
        self._io_client = FileIOClient()

    async def benchmark(
            self,
            hosts: list[str] | None = None,
            count: int = 1,
            input_file: str | None = None,
            output_file: str | None = None
    ):
        """ Запускает тестирование доступности хостов """
        target_hosts = hosts if hosts else self._io_client.read_lines(input_file)
        if not target_hosts:
            raise HttpBenchBaseException("Список хостов пуст")

        target_hosts = validate_hosts_list(target_hosts)

        async with self._http_client as http_client:
            coroutines = []
            for host in target_hosts:
                for _ in range(count):
                    coroutines.append(http_client.get(host))

            results = {host: [] for host in target_hosts}
            for completed in asyncio.as_completed(coroutines): # Получает ответ от корутин по мере их выполнения
                response = await completed
                results[response['url']].append(response)

        output_text = format_benchmark_report(results)

        if output_file:
            self._io_client.write_lines(output_file, [output_text])
            print(f"Результаты сохранены в {output_file}")
        else:
            print(output_text)
