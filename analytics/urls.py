from django.urls.conf import path
from analytics.views.poll_detail import poll_analytics, piechart_data, bargraph_data, linegraph_data, question_analytics, question_correct_analytics, poll_correct_analytics, poll_correct_linegraph_data, poll_correct_bargraph_data, poll_correct_piechart_data
from analytics.views.download_csv import download_csv

urlpatterns = [
    path('polls/<int:poll_id>/', poll_analytics, name='poll_analytics'),
    path('polls/<int:poll_id>/piechart_data/', piechart_data, name='piechart_data'),
    path('polls/<int:poll_id>/bargraph_data/', bargraph_data, name='bargraph_data'),
    path('polls/<int:poll_id>/linegraph_data/', linegraph_data, name='linegraph_data'),
    path('polls/<int:poll_id>/download_csv/', download_csv, name='download_csv'),
    path('questions/<int:question_id>/analytics/', question_analytics, name='question_analytics'),
    path('questions/<int:question_id>/correct_analytics/', question_correct_analytics, name='question_correct_analytics'),
    path('polls/<int:poll_id>/correct_analytics/', poll_correct_analytics, name='poll_correct_analytics'),
    path('polls/<int:poll_id>/correct_piechart_data/', poll_correct_piechart_data, name='poll_correct_piechart_data'),
    path('polls/<int:poll_id>/correct_bargraph_data/', poll_correct_bargraph_data, name='poll_correct_bargraph_data'),
]

