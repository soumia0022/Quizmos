from django.urls.conf import path
from response_management.views.lecturer_poll_list import lecturer_poll_list
from response_management.views.poll_detail import poll_detail, piechart_data, bargraph_data, linegraph_data
from response_management.views.download_csv import download_csv

urlpatterns = [
    path('polls/', lecturer_poll_list, name='lecturer_poll_list'),
    path('polls/<int:poll_id>/', poll_detail, name='poll_detail'),
    path('polls/<int:poll_id>/piechart_data/', piechart_data, name='piechart_data'),
    path('polls/<int:poll_id>/bargraph_data/', bargraph_data, name='bargraph_data'),
    path('polls/<int:poll_id>/linegraph_data/', linegraph_data, name='linegraph_data'),
    path('polls/<int:poll_id>/download_csv/', download_csv, name='download_csv'),
]