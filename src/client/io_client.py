import os
from src.exceptions import HttpBenchBaseException


class FileIOClient:
    def read_lines(self, filepath: str) -> list[str]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл {filepath} не найден")
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise HttpBenchBaseException(f"Файл {filepath} пуст")
        return lines

    @staticmethod
    def write_lines(filepath: str, lines: list[str]):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
