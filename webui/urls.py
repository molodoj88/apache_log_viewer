from django.urls import path
from .views import *


urlpatterns = [
    path('', records_list, name='records_list_url'),
]