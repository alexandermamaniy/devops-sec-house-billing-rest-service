import factory
from faker import Faker

from buddy_groups.models import BuddyGroup
from buddy_profiles.models import BuddyProfile
from users.models import User

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = fake.email()
    password = fake.password()
    is_staff = False
    is_superuser = False

class BuddyProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuddyProfile

    user = factory.SubFactory(UserFactory)
    full_name = fake.name()
    picture_url = fake.image_url()

#
# class BuddyGroupFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = BuddyGroup
#
#     name = fake.name()
#
#     @factory.post_generation
#     def group_members(self, create, extracted, **kwargs):
#         if not create:
#             return
#
#         if extracted:
#             for member in extracted:
#                 self.group_members.add(member)
#
#     @factory.post_generation
#     def group_admins(self, create, extracted, **kwargs):
#         if not create:
#             return
#
#         if extracted:
#             for admin in extracted:
#                 self.group_admins.add(admin)