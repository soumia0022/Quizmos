from django.urls.conf import path
from analytics.views.poll_detail import (
    poll_analytics,
    poll_graph_data,
    question_analytics,
    question_correct_analytics,
    poll_correct_analytics
)
from analytics.views.download_csv import download_csv

urlpatterns = [
    path('polls/<int:poll_id>/', poll_analytics, name='poll_analytics'),
    path('polls/<int:poll_id>/download_csv/', download_csv, name='download_csv'),
    path('polls/<int:poll_id>/chart_data/<str:chart_type>/', poll_graph_data, name='poll_graph_data'),
    path('polls/<int:poll_id>/piechart_data/', lambda request, poll_id: poll_graph_data(request, poll_id, 'pie'), name='piechart_data'),
    path('polls/<int:poll_id>/bargraph_data/', lambda request, poll_id: poll_graph_data(request, poll_id, 'bar'), name='bargraph_data'),
    path('polls/<int:poll_id>/linegraph_data/', lambda request, poll_id: poll_graph_data(request, poll_id, 'line'), name='linegraph_data'),
    path('questions/<int:question_id>/analytics/', question_analytics, name='question_analytics'),
    path('questions/<int:question_id>/correct_analytics/', question_correct_analytics, name='question_correct_analytics'),
    path('polls/<int:poll_id>/correct_analytics/<str:chart_type>/', poll_correct_analytics, name='poll_correct_analytics_with_type'),
    path('polls/<int:poll_id>/correct_analytics/', lambda request, poll_id: poll_correct_analytics(request, poll_id, 'default'), name='poll_correct_analytics'),
    path('polls/<int:poll_id>/correct_piechart_data/', lambda request, poll_id: poll_correct_analytics(request, poll_id, 'pie'), name='poll_correct_piechart_data'),
    path('polls/<int:poll_id>/correct_bargraph_data/', lambda request, poll_id: poll_correct_analytics(request, poll_id, 'bar'), name='poll_correct_bargraph_data'),
]