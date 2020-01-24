from django.db import models


# Create your models here.
class LogRecord(models.Model):
    date = models.DateTimeField()
    ip_addr = models.GenericIPAddressField()
    http_method = models.CharField(max_length=10)
    request_uri = models.URLField()
    error_code = models.PositiveSmallIntegerField()
    response_size = models.SmallIntegerField()

    def get_formatted_date(self):
        return self.date.strftime("%d/%m/%Y %H:%M:%S")
