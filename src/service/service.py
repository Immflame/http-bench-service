from src.client import HTTPClient, FileIOClient
from src.collectors import StatCollector


class BenchmarkService:
    """ Бизнес-логика """
    def __init__(self):
        self._HTTPClient = HTTPClient()
        self._IOClient = FileIOClient()
        self._StatCollector = StatCollector()

    def start_test(self, hosts, count_requests, input_file, output_file):
        pass

    def print_results(self):
        pass

    def _save_results(self):
        pass
