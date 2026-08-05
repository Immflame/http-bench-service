from src.exceptions import HttpBenchBaseException


class FileIOClient:
    """ Клиент для записи и чтения из файлов """
    @staticmethod
    def read_lines(filepath: str) -> list[str]:
        """ Читает из файла построчко и возвращает список строк """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError as e:
            raise HttpBenchBaseException(f"Файл {filepath} не найден")

        if not lines:
            raise HttpBenchBaseException(f"Файл {filepath} пуст")
        return lines

    @staticmethod
    def write_lines(filepath: str, lines: list[str]):
        """ Записывает в файл """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
