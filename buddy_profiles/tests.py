from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import ast
from users.models import User
from buddy_profiles.models import BuddyProfile
class CreateBuddyProfileModelTest(APITestCase):

    def setUp(self):

        # create Buddy Profle
        self.user = User.objects.create_user(email='contact@alexander.com', password="user")
        self.user.save()
        self.buddyProfile = BuddyProfile.objects.create(user=self.user, full_name="Alexander Contact", picture_url=None)
        self.buddyProfile.save()
    #
    def test_create_user(self):
        user = User.objects.get(email='contact@alexander.com')
        buddy_profile = BuddyProfile.objects.get(user=user)

        self.assertIsNotNone(buddy_profile)
        self.assertEqual(self.buddyProfile, buddy_profile)
        self.assertEqual(buddy_profile.full_name, 'Alexander Contact')
        # self.assertIsNone(buddy_profile.picture_url)