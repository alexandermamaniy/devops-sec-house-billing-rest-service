import pytest
from users.models import User
from faker import Faker

fake = Faker()
@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        self.fake_member_email = fake.email()

        self.fake_member_password = fake.password()

        user = User.objects.create_user(email=self.fake_member_email, password=self.fake_member_password )
        assert user.email == self.fake_member_email
        assert user.check_password(self.fake_member_password )
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self):
        self.fake_admin_email = fake.email()
        self.fake_admin_password = fake.password()

        superuser = User.objects.create_superuser(email=self.fake_admin_email, password=self.fake_admin_password)
        assert superuser.email == self.fake_admin_email
        assert superuser.check_password(self.fake_admin_password)
        assert superuser.is_staff
        assert superuser.is_superuser