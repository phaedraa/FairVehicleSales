from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^vehicle_sales/$', views.vehicle_sales_list),
    url(r'^vehicle_sales/(?P<sale_id>[0-9]+)$', views.vehicle_sales_detail),
    url(r'^vehicle_sales/car/(?P<vin>[0-9A-Za-z]+)$', views.vehicle_sales_car_detail)
]
