from django.shortcuts import render
from logparser.models import *
from .utils import get_statistics, apply_filters, paginate
from django.db.utils import OperationalError


RECORDS_PER_PAGE_LIST = [10, 20, 50, 100]
RECORDS_PER_PAGE = int(RECORDS_PER_PAGE_LIST[0])


def records_list(request):
    """
    Main view of UI
    """
    # Get records per page from session
    global RECORDS_PER_PAGE
    records_per_page = request.session.get("records_per_page")
    if not records_per_page:
        records_per_page = RECORDS_PER_PAGE
        request.session["records_per_page"] = records_per_page

    # Start filters descriptions
    ip_address = request.GET.get('ipaddr', '')
    start_date = request.GET.get('startdate', '')
    end_date = request.GET.get('enddate', '')
    http_method = request.GET.get('method', '')
    uri = request.GET.get('uri', '')
    response_code = request.GET.get('response_code', '')
    # End filters descriptions

    # Get all records
    try:
        records = LogRecord.objects.all()
        all_records_num = len(records)
        if records:
            pass
    except OperationalError:
        context = {"empty": True}
    else:
        # Get all statistics
        all_statistics = get_statistics(records, heading="All records statistics")

        # Apply filters if exists
        records, href = apply_filters(records,
                                      ip_address=ip_address,
                                      http_method=http_method,
                                      response_code=response_code,
                                      uri=uri,
                                      start_date=start_date,
                                      end_date=end_date)

        # Attributes are passed to the context to save filter inputs values
        attributes = {"ip_address": ip_address,
                      "start_date": start_date,
                      "end_date": end_date,
                      "http_method": http_method,
                      "uri": uri,
                      "response_code": response_code}

        all_dates = [record.date for record in LogRecord.objects.all()]
        min_date = min(all_dates).strftime("%Y-%m-%d")
        max_date = max(all_dates).strftime("%Y-%m-%d")

        # Paginate
        _records_per_page = request.GET.get('records_per_page', '')
        if _records_per_page:
            records_per_page = int(_records_per_page)
            request.session["records_per_page"] = records_per_page
        page_number = request.GET.get('page', 1)
        page, number_of_pages = paginate(records, records_per_page, page_number)

        # Get filtered statistics
        if len(records) != all_statistics["total_records"]["value"]:
            filtered_statistics = get_statistics(records, heading="Filtered records statistics")
        else:
            filtered_statistics = {"empty": True}

        context = {"empty": False,
                   "page": page,
                   "number_of_pages": number_of_pages,
                   "min_date": min_date,
                   "max_date": max_date,
                   "href": href,
                   "attributes": attributes,
                   "records_per_page": records_per_page,
                   "records_per_page_list": RECORDS_PER_PAGE_LIST,
                   "statistics": {"all": all_statistics,
                                  "filtered": filtered_statistics}}

    return render(request, "webui/index.html", context=context)
