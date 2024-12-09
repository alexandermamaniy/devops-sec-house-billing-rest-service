from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from buddy_profiles.models import BuddyProfile
from buddy_profiles.serializers import BuddyProfileSerializer, BuddyMemberOfAGroupRetrieveSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class BuddyProfileListCreateView(generics.ListCreateAPIView):
    queryset = BuddyProfile.objects.all()
    serializer_class = BuddyProfileSerializer


class RetrieveUserAPIView(RetrieveAPIView):
    serializer_class = BuddyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = BuddyProfile.objects.get(user=self.request.user )
        self.check_object_permissions(self.request, obj)
        return obj


class RetrieveMemberAndAdminsOfAGroupAPIView(RetrieveAPIView):
    serializer_class = BuddyMemberOfAGroupRetrieveSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        group_id = self.kwargs.get('pk')
        members_of_group = BuddyProfile.objects.filter(group_members__id=group_id)
        admins_of_group = BuddyProfile.objects.filter(group_admins__id=group_id)

        obj =  {'members_of_group':members_of_group, 'admins_of_group':admins_of_group}
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset, context={'request': request})
        return Response(serializer.data)
