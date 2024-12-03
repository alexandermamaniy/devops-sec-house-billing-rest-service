from rest_framework.generics import RetrieveAPIView, CreateAPIView

from buddy_groups.models import BuddyGroup
from buddy_groups.serializers import BuddyGroupRequestSerializer, \
    BuddyGroupRetrieveRequestSerializer, CreateGroupUserAuthenticatedSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from buddy_profiles.models import BuddyProfile



class RetrieveGroupAPIView(RetrieveAPIView):
    serializer_class = BuddyGroupRetrieveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_authenticated = BuddyProfile.objects.get(user=self.request.user)
        group_members = BuddyGroup.objects.filter(groupmembers__buddy_profile_member=user_authenticated)
        group_admins = BuddyGroup.objects.filter(groupadmins__buddy_profile_admin=user_authenticated)
        obj =  {'groups_that_belong':group_members, 'groups_that_manage':group_admins}
        # self.check_object_permissions(self.request, obj)
        return obj

class CreateGroupOfUserAuthenticated(CreateAPIView):
    serializer_class = CreateGroupUserAuthenticatedSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['group_members'] = self.request.data.get('group_members')
        context['admin'] = self.request.user
        return context

    @extend_schema(
        request=BuddyGroupRequestSerializer,
        responses={201: CreateGroupUserAuthenticatedSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
