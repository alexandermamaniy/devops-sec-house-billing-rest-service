import pytest
from django.contrib.auth import get_user_model
from buddy_groups.models import BuddyGroup, GroupMembers, GroupAdmins
from buddy_profiles.models import BuddyProfile

User = get_user_model()

@pytest.mark.django_db
class TestBuddyGroupModel:

    def test_create_buddy_group(self):
        buddy_group = BuddyGroup.objects.create(name='Test Group')
        assert buddy_group.name == 'Test Group'

    def test_update_buddy_group(self):
        buddy_group = BuddyGroup.objects.create(name='Test Group')
        buddy_group.name = 'Updated Group'
        buddy_group.save()
        assert buddy_group.name == 'Updated Group'

    def test_add_group_member(self):
        user = User.objects.create_user(email='member@example.com', password='password123')
        member = BuddyProfile.objects.create(full_name='Member', user=user)
        buddy_group = BuddyGroup.objects.create(name='Test Group')
        GroupMembers.objects.create(group_belong_to=buddy_group, buddy_profile_member=member)
        assert buddy_group.groupmembers_set.count() == 1

    def test_add_group_admin(self):
        user = User.objects.create_user(email='admin@example.com', password='password123')
        admin = BuddyProfile.objects.create(full_name='Admin', user=user)
        buddy_group = BuddyGroup.objects.create(name='Test Group')
        GroupAdmins.objects.create(group_belong_to=buddy_group, buddy_profile_admin=admin, is_admin_a_member=True)
        assert buddy_group.groupadmins_set.count() == 1