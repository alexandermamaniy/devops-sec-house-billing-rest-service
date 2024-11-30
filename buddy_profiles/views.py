from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from buddy_profiles.models import BuddyProfile
from buddy_profiles.serializers import BuddyProfileSerializer, BuddyMemberOfAGroupRetrieveSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class BuddyProfileListCreateView(generics.ListCreateAPIView):
    queryset = BuddyProfile.objects.all()
    serializer_class = BuddyProfileSerializer


class BuddyProfileRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BuddyProfile.objects.filter(is_active=True)
    serializer_class = BuddyProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.deleted_date = timezone.now()
        instance.save()
        user = instance.user
        user.is_active = False
        user.deleted_date = timezone.now()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RetrieveUserAPIView(RetrieveAPIView):
    serializer_class = BuddyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = BuddyProfile.objects.get(user=self.request.user )
        self.check_object_permissions(self.request, obj)
        return obj

class CreateIserAPIView(CreateAPIView):
    serializer_class = BuddyProfileSerializer
    permission_classes = [IsAuthenticated]


class RetrieveMemberAndAdminsOfAGroupAPIView(RetrieveAPIView):
    serializer_class = BuddyMemberOfAGroupRetrieveSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        #Validate that user authenticated must be an admin of the group
        # user_authenticated = BuddyProfile.objects.get(user=self.request.user)
        group_id = self.kwargs.get('pk')
        members_of_group = BuddyProfile.objects.filter(group_members__id=group_id)
        admins_of_group = BuddyProfile.objects.filter(group_admins__id=group_id)

        obj =  {'members_of_group':members_of_group, 'admins_of_group':admins_of_group}
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        # Get the model instance
        queryset = self.get_object()

        # Instantiate the serializer
        serializer = self.get_serializer(queryset, context={'request': request})

        # serializer = BuddyGroupRetrieveRequestSerializer(queryset, context={'request': request})

        # Return the serialized data
        return Response(serializer.data)
