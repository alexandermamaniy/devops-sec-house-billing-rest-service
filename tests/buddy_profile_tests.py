import pytest
from django.urls import reverse
from .factories import BuddyProfileFactory, BuddyGroupFactory

pytestmark = pytest.mark.django_db

class TestBuddyProfileCRUD:
    profile_list_create_url = reverse('buddy_profiles:buddyprofile-list-create')

    def test_create_profile(self, api_client):
        data = {
                  "user": {
                    "email": "user1@user.com",
                    "password": "user"
                  },
                  "full_name": "user1"
                }

        response = api_client.post(self.profile_list_create_url, data,  format='json')
        assert response.status_code == 201
        returned_json = response.json()
        assert 'id' in returned_json
        assert returned_json['full_name'] == data['full_name']
        assert returned_json['user']["email"] == data['user']["email"]

    def test_list_profiles(self, api_client):
        BuddyProfileFactory.create_batch(5)
        response = api_client.get(self.profile_list_create_url)
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_retrieve_profile(self, api_client):
        profile = BuddyProfileFactory()
        user = profile.user
        api_client.force_authenticate(user=user)

        response = api_client.get(reverse('buddy_profiles:buddyprofile-detail-me'))
        assert response.status_code == 200
        returned_json = response.json()
        assert 'id' in returned_json
        assert returned_json['full_name'] == profile.full_name
        assert returned_json['user']["email"] == profile.user.email

    def test_retrieve_member_and_admins_of_a_group(self, api_client):
        member1 = BuddyProfileFactory()
        member2 = BuddyProfileFactory()
        admin = BuddyProfileFactory()
        group = BuddyGroupFactory(group_members=[member1, member2], group_admins=[admin])

        # Authenticate the API client
        api_client.force_authenticate(user=admin.user)

        # Make a GET request to the view
        url = reverse('buddy_profiles:member-and-admins-of-a-group', args=[group.id])
        response = api_client.get(url)

        # Assert the response status code and content
        assert response.status_code == 200
        returned_json = response.json()
        assert 'members_of_group' in returned_json
        assert 'admins_of_group' in returned_json
        assert len(returned_json['members_of_group']) == 2
        assert len(returned_json['admins_of_group']) == 1
        assert returned_json['members_of_group'][0]['id'] == str(member1.id)
        assert returned_json['members_of_group'][1]['id'] == str(member2.id)
        assert returned_json['admins_of_group'][0]['id'] == str(admin.id)

