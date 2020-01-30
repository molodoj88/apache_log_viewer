from django.core.management.base import BaseCommand
import tempfile
import requests
from tqdm import tqdm
from ._parser import _Parser
from logparser.models import LogRecord
from apache_log_parser import LineDoesntMatchException


class Command(BaseCommand):
    help = 'Downloads and parses apache log file'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        url = options['url'][0]
        # Make parser
        parser = Parser()
        # Download file
        lines = parser.download_file(url)
        # Parse data
        parsed_data = parser.parse_lines(lines)
        # Save to database
        parser.save_records(parsed_data)


class Parser:
    """
    Main parser class. Allows to download file,
    parse and save data into database.
    """
    def __init__(self, parser=None):
        self.parser: _Parser = parser or _Parser()

    @staticmethod
    def download_file(url: str) -> list:
        """
        Downloads a file with apache access log
        :param url: url to download file
        :return: lines of a file (list)
        """
        r = requests.get(url, stream=True)
        total_size = int(r.headers['content-length'])
        chunk_size = 1024
        unit = 'kb'
        # File size in kb
        total = total_size / chunk_size
        with tempfile.TemporaryFile() as file:
            with tqdm(total=total, unit=unit, desc='Download') as pbar:
                for data in r.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    pbar.update(1)
            file.seek(0)
            # Read downloaded file and extract rows from it
            data = file.read().decode('utf-8')
            lines = data.split('\n')
            return lines

    def parse_lines(self, lines: list) -> list:
        """
        Parse lines in log file
        :param lines: list of lines read from file
        :return: list of parsed lines as dicts
        """
        parsed_data = []
        with tqdm(total=len(lines), desc='Parsing', unit='lines') as pbar:
            for n, line in enumerate(lines):
                try:
                    parsed_line: dict = self.parser.parse(line)
                except LineDoesntMatchException:
                    continue
                parsed_data.append(parsed_line)
                pbar.update(1)
        return parsed_data

    def save_records(self, parsed_data: list):
        """
        Saves records to database
        :param parsed_data: list of parsed data (dicts)
        """
        if parsed_data:
            with tqdm(total=len(parsed_data), desc='Save to database', unit='records') as pbar:
                for record in parsed_data:
                    self.save_log_record(record)
                    pbar.update(1)


    @staticmethod
    def save_log_record(parsed_data: dict):
        """
        Save on record to database
        :param parsed_data: dict representation of one parsed row of log
        :return:
        """
        record = LogRecord()
        record.date = parsed_data['date']
        record.ip_addr = parsed_data['ip_address']
        record.request_uri = parsed_data['request_url']
        record.error_code = parsed_data['status']
        record.http_method = parsed_data['http_method']
        record.response_size = parsed_data['response_length']
        try:
            record.save()
        except Exception as e:
            return
