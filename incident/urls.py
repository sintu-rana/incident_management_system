from django.urls import path
from incident.views import *

## Define here our urls

urlpatterns = [
    path("signup-user/", SignUpAPIView.as_view(), name="create-user"),
    path("login-user/", LoginAPIView.as_view(), name="login-user-get-token"),
    path("create_incident/", CreateIncidentAPIView.as_view(), name="create-incident"),
    path("get_incident/", GetncidentDetailsView.as_view(), name="get-incident_details"),
    path("get-update-incident/<int:pk>/", GetUpdateIncidentDetails.as_view(), name="get-update-incident-details"),
    path("search-incident/", SearchIncidentAPIView.as_view(), name="search-incident-information")
]