import factory
from faker import Faker

from buddy_groups.models import BuddyGroup, GroupMembers, GroupAdmins
from buddy_profiles.models import BuddyProfile
from users.models import User

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = fake.password()
    is_staff = False
    is_superuser = False

class BuddyProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuddyProfile

    user = factory.SubFactory(UserFactory)
    full_name = fake.name()
    picture_url = fake.image_url()


class BuddyGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuddyGroup

    name = fake.name()

    @factory.post_generation
    def group_members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                GroupMembers.objects.create(group_belong_to=self, buddy_profile_member=member)

    @factory.post_generation
    def group_admins(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for admin in extracted:
                GroupAdmins.objects.create(group_belong_to=self, buddy_profile_admin=admin)