from django.urls import path
from .views import trace_ip, ip_statistics


urlpatterns = [
    path('traces/', trace_ip, name='trace-ip'),
    path('statistics/', ip_statistics, name='statistics'),
]
