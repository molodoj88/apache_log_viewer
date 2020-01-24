from apache_log_parser import Parser


class _Parser:
    """
    Implements main log parser functionality
    """
    def __init__(self, log_format=None):
        if log_format:
            self.LOG_FORMAT = log_format
        else:
            self.LOG_FORMAT = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""
        self.parser = Parser(self.LOG_FORMAT)

    def parse(self, string: str) -> dict:
        """
        Parse data from string of log record
        :param string: log record
        :return:
        """
        data = self.parser.parse(string)
        return self._process_parsed_data(data)

    @staticmethod
    def _process_parsed_data(data: dict) -> dict:
        """
        Casts the data to a form suitable
        for saving to the database
        :param data: one parsed record (dict)
        :return: new data record (dict)
        """
        new_data = dict()
        new_data['ip_address'] = data['remote_host']
        new_data['date'] = data['time_received_tz_datetimeobj']
        new_data['http_method'] = data['request_method']
        new_data['request_url'] = data['request_url']
        new_data['status'] = data['status']
        new_data['response_length'] = data['response_bytes_clf']
        return new_data
