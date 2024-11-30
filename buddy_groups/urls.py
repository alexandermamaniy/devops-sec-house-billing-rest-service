from django.urls import path
from .views import (
    RetrieveGroupAPIView, CreateGroupOfUserAuthenticated,
)

urlpatterns = [
    path('buddy-groups/me', RetrieveGroupAPIView.as_view(), name='buddy-group-list-me'),
    path('buddy-groups/', CreateGroupOfUserAuthenticated.as_view(), name='buddy-group-create-me'),
    # path('buddy-groups/<uuid:pk>/', BuddyGroupRetrieveUpdateDestroyView.as_view(), name='buddy-group-detail'),

]