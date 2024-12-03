from django.urls import path
from buddy_profiles.views import BuddyProfileListCreateView, RetrieveUserAPIView, RetrieveMemberAndAdminsOfAGroupAPIView

app_name = "buddy_profiles"

urlpatterns = [
    path('buddy-profiles/me/', RetrieveUserAPIView.as_view(), name='buddyprofile-detail-me'),
    path('buddy-profiles/', BuddyProfileListCreateView.as_view(), name='buddyprofile-list-create'),
    path('buddy-profiles/group/<uuid:pk>/', RetrieveMemberAndAdminsOfAGroupAPIView.as_view(), name='member-and-admins-of-a-group'),
]
