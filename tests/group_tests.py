import pytest
from django.urls import reverse
from .factories_models_tests import BuddyProfileFactory, BuddyGroupFactory

pytestmark = pytest.mark.django_db

class TestBuddyGroupCRUD:
    retrieve_buddy_group = reverse('buddy_groups:buddy-group-list-me')
    create_buddy_group = reverse('buddy_groups:buddy-group-create-me')

    def test_create_group(self, api_client):
        data = {
                  "name": "group_test_name",
                  "group_members": [
                      BuddyProfileFactory().id,
                      BuddyProfileFactory().id
                  ],
                  "group_admins": [
                      BuddyProfileFactory().id
                  ]
                }
        profile = BuddyProfileFactory()
        user = profile.user
        api_client.force_authenticate(user=user)

        response = api_client.post(self.create_buddy_group, data,  format='json')
        assert response.status_code == 201
        returned_json = response.json()
        assert 'id' in returned_json
        assert returned_json['name'] == data['name']

    def test_retrieve_buddy_groups(self, api_client):
        BuddyGroupFactory.create_batch(5)
        profile = BuddyProfileFactory()
        user = profile.user
        api_client.force_authenticate(user=user)
        response = api_client.get(self.retrieve_buddy_group)
        assert response.status_code == 200