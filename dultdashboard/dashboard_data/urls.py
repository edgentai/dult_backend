from django.urls import path

from dashboard_data.api import LineChartDataQuery

urlpatterns = [
    path(
        r"dashboard-data/line-chart/",
        LineChartDataQuery.as_view()
    ),
]