from django.urls import path
from .views import (
    RetrieveGroupAPIView, CreateGroupOfUserAuthenticated,
)

app_name = "buddy_groups"

urlpatterns = [
    path('buddy-groups/me', RetrieveGroupAPIView.as_view(), name='buddy-group-list-me'),
    path('buddy-groups/', CreateGroupOfUserAuthenticated.as_view(), name='buddy-group-create-me'),
]