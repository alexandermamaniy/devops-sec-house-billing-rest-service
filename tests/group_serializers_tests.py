import pytest
from django.contrib.auth import get_user_model
from buddy_groups.models import BuddyGroup, GroupMembers, GroupAdmins
from buddy_groups.serializers import BuddyGroupSerializer
from buddy_profiles.models import BuddyProfile
from faker import Faker

fake = Faker()
User = get_user_model()

@pytest.mark.django_db
class TestBuddyGroupSerializer:

    def test_create_buddy_group(self):
        self.fake_member_email = fake.email()
        self.fake_admin_email = fake.email()

        self.fake_admin_password = fake.password()
        self.fake_member_password = fake.password()

        user_member = User.objects.create_user(email=self.fake_member_email, password=self.fake_member_password)
        user_admin = User.objects.create_user(email=self.fake_admin_email, password=self.fake_admin_password)
        member = BuddyProfile.objects.create(full_name='Member', user=user_member)
        admin = BuddyProfile.objects.create(full_name='Admin', user=user_admin)
        data = {
            'name': 'Test Group',
            'group_members': [{'buddy_profile_member': member.id}],
            'group_admins': [{'buddy_profile_admin': admin.id, 'is_admin_a_member': True}]
        }
        context = {'group_members': [member.id], 'group_admins': [admin.id]}
        serializer = BuddyGroupSerializer(data=data, context=context)
        assert serializer.is_valid()
        buddy_group = serializer.save()
        assert buddy_group.name == data['name']
        assert buddy_group.groupmembers_set.count() == 1
        assert buddy_group.groupadmins_set.count() == 1

    def test_update_buddy_group(self):
        self.fake_member_email = fake.email()
        self.fake_admin_email = fake.email()

        self.fake_admin_password = fake.password()
        self.fake_member_password = fake.password()
        user_member = User.objects.create_user(email=self.fake_member_email, password='password123')
        user_admin = User.objects.create_user(email=self.fake_admin_email, password=self.fake_admin_password)
        buddy_group = BuddyGroup.objects.create(name='Test Group')
        member = BuddyProfile.objects.create(full_name='Member', user=user_member)
        admin = BuddyProfile.objects.create(full_name='Admin', user=user_admin)
        GroupMembers.objects.create(group_belong_to=buddy_group, buddy_profile_member=member)
        GroupAdmins.objects.create(group_belong_to=buddy_group, buddy_profile_admin=admin, is_admin_a_member=True)
        data = {
            'name': 'Updated Group',
            'group_members': [{'buddy_profile_member': member.id}],
            'group_admins': [{'buddy_profile_admin': admin.id, 'is_admin_a_member': True}]
        }
        context = {'group_members': [member.id], 'group_admins': [admin.id]}
        serializer = BuddyGroupSerializer(buddy_group, data=data, context=context)
        assert serializer.is_valid()
        updated_buddy_group = serializer.save()
        assert updated_buddy_group.name == data['name']
        assert updated_buddy_group.groupmembers_set.count() == 1
        assert updated_buddy_group.groupadmins_set.count() == 1