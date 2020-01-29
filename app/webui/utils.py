from django.db.models import Count, Avg
from datetime import datetime
from django.core.paginator import Paginator
from collections import OrderedDict


def get_statistics(records, heading="Statistics"):
    """
    Get statistics of records set.
    :param records: QuerySet with log records
    :param heading: Title of statistics block
    :return: dict with computed stats
    """
    total_ip_addresses = len(records.values('ip_addr').distinct())
    all_ip_addresses_count = records.values('ip_addr').annotate(count=Count('ip_addr'))
    all_ip_addresses_count_list = [(record['ip_addr'], int(record['count'])) for record in all_ip_addresses_count]
    all_ip_addresses_count_list.sort(key=lambda x: x[1], reverse=True)
    most_common_ips = OrderedDict()
    if len(all_ip_addresses_count_list) >= 3:
        for i in range(3):
            most_common_ips[all_ip_addresses_count_list[i][0]] = all_ip_addresses_count_list[i][1]
    else:
        for i in all_ip_addresses_count_list:
            most_common_ips[i[0]] = i[1]
    all_methods_count = records.values('http_method').annotate(count=Count('http_method'))
    avg_response_size = records.aggregate(avg=Avg('response_size'))
    return {
                "empty": False,  # need to render statistics block from template. See 'statistics.html' in templates dir
                "heading": heading,
                "total_records": {"name": "Total records", "value": len(records)},
                "total_ip_addresses": {"name": "Total IP-addresses", "value": total_ip_addresses},
                "three_most_common_ip": {"name": "Most common IPs", "value": most_common_ips},
                "total_methods_count": {"name": "HTTP methods",
                                        "value": {i['http_method']: i['count'] for i in all_methods_count}
                                        },
                "avg_response_size": {"name": "Avg. response size", "value": avg_response_size["avg"]}
            }


def apply_filters(records, **kwargs):
    """
    Applies filters (if exists) to all db records
    :param records: all log records from database
    :param kwargs: ip_address, http_method, uri, response_code, start_date, end_date,
    :return: tuple (records, href)
    """

    date_format = "%Y-%m-%d %H:%M:%S"

    ip_address = kwargs.get('ip_address', '')
    http_method = kwargs.get('http_method', '')
    uri = kwargs.get('uri', '')
    response_code = kwargs.get('response_code', '')
    start_date = kwargs.get('start_date', '')
    end_date = kwargs.get('end_date', '')

    href = ''

    if ip_address:
        records = records.filter(ip_addr__icontains=ip_address)
        href += "&ipaddr={}".format(ip_address)
    if http_method:
        records = records.filter(http_method__icontains=http_method)
        href += "&method={}".format(http_method)
    if uri:
        records = records.filter(request_uri__icontains=uri)
        href += "&uri={}".format(uri)
    if response_code:
        records = records.filter(error_code__icontains=response_code)
        href += "&response_code={}".format(response_code)
    if start_date and end_date:
        records = records.filter(date__gte=datetime.strptime(start_date + " 00:00:00", date_format))
        records = records.filter(date__lte=datetime.strptime(end_date + " 23:59:59", date_format))
        href += "&startdate={}&enddate={}".format(start_date, end_date)
    if start_date and not end_date:
        records = records.filter(date__gte=datetime.strptime(start_date + " 00:00:00", date_format))
        href += "&startdate={}".format(start_date)
    if not start_date and end_date:
        records = records.filter(date__lte=datetime.strptime(end_date + " 23:59:59", date_format))
        href += "&enddate={}".format(end_date)

    return records, href


def paginate(records, records_per_page, page_number):
    """
    Make pagination
    :param records: QuerySet with records passed
    :param records_per_page: number of records per page
    :param page_number: current page number
    :return: page object, number of pages (int)
    """
    paginator = Paginator(records, records_per_page)
    number_of_pages = paginator.num_pages
    page = paginator.get_page(page_number)
    return page, number_of_pages
