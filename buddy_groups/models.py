from django.db import models
import uuid
from buddy_profiles.models import BuddyProfile
from core.models import TimeStampedModel


class BuddyGroup(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Group name', max_length=255, blank=False, null=False)
    group_members = models.ManyToManyField(BuddyProfile, through="GroupMembers", related_name='group_members')
    group_admins = models.ManyToManyField(BuddyProfile, through="GroupAdmins", related_name='group_admins')

    def __str__(self):
        return f'{self.name}'

class GroupMembers(TimeStampedModel):
    buddy_profile_member = models.ForeignKey(BuddyProfile, on_delete=models.CASCADE)
    group_belong_to = models.ForeignKey(BuddyGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.buddy_profile_member.full_name} - {self.group_belong_to.name} '



class GroupAdmins(TimeStampedModel):
    buddy_profile_admin = models.ForeignKey(BuddyProfile, on_delete=models.CASCADE)
    group_belong_to = models.ForeignKey(BuddyGroup, on_delete=models.CASCADE)
    # revisar si eliminar este campo o no
    is_admin_a_member = models.BooleanField(default=False)

