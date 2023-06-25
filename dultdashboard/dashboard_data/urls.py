from django.urls import path

from dashboard_data.api import LineChartDataQuery, BarGraphDataQuery, CardDataAPI, TweetDataAPI

urlpatterns = [
    path(
        r"dashboard-data/line-chart/",
        LineChartDataQuery.as_view()
    ),
    path(
        r"dashboard-data/bar-graph/",
        BarGraphDataQuery.as_view()
    ),
    path(
        r"dashboard-data/card-data/",
        CardDataAPI.as_view()
    ),
    path(
        r"dashboard-data/tweet-data/",
        TweetDataAPI.as_view()
    ),
]