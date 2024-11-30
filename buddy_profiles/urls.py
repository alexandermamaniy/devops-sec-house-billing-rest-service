from django.urls import path
from buddy_profiles.views import BuddyProfileListCreateView, BuddyProfileRetrieveUpdateDestroy, RetrieveUserAPIView, \
    CreateIserAPIView, RetrieveMemberAndAdminsOfAGroupAPIView

urlpatterns = [
    # path('buddy-profiles/', CreateIserAPIView.as_view(), name='buddyprofile-create'),
    path('buddy-profiles/me/', RetrieveUserAPIView.as_view(), name='buddyprofile-detail-me'),

    ## implement middleware for only admins and refactor generic views
    path('buddy-profiles/', BuddyProfileListCreateView.as_view(), name='buddyprofile-list-create'),

    path('buddy-profiles/group/<uuid:pk>/', RetrieveMemberAndAdminsOfAGroupAPIView.as_view(), name='member-and-admins-of-a-group'),

    # path('buddy-profiles/<uuid:pk>/', BuddyProfileRetrieveUpdateDestroy.as_view(), name='buddyprofile-detail'),
]
