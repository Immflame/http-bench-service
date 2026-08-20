from http_bench_service.exceptions import BenchmarkFileClientException


class FileClient:
    @staticmethod
    def read_lines(filepath: str) -> list[str]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            raise BenchmarkFileClientException(f"Файл {filepath} не найден")
        if not lines:
            raise BenchmarkFileClientException(f"Файл {filepath} пуст")
        return lines

    @staticmethod
    def write_lines(filepath: str, lines: list[str]):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
