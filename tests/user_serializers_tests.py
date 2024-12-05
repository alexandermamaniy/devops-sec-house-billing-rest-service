import pytest
from users.models import User
from users.serializers import UserSerializer
from faker import Faker

fake = Faker()
@pytest.mark.django_db
class TestUserSerializer:

    def test_create_user(self):
        self.fake_member_email = fake.email()
        self.fake_member_password = fake.password()

        self.fake_member_updated_email = fake.email()
        self.fake_member_updated_password = fake.password()

        data = {
            'email': self.fake_member_email,
            'password': self.fake_member_password ,
            'is_active': True,
            'timezone': 'UTC'
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == data['email']
        assert user.check_password(data['password'])
        assert user.is_active == data['is_active']
        assert user.timezone == data['timezone']

    def test_update_user(self):
        self.fake_member_email = fake.email()
        self.fake_member_password = fake.password()

        self.fake_member_updated_email = fake.email()
        self.fake_member_updated_password = fake.password()

        user = User.objects.create_user(email=self.fake_member_email, password=self.fake_member_password )
        data = {
            'email': self.fake_member_updated_email ,
            'password': self.fake_member_updated_password,
            'is_active': False,
            'timezone': 'Europe/London'
        }
        serializer = UserSerializer(user, data=data)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.email == data['email']
        assert updated_user.check_password(data['password'])
        assert updated_user.is_active == data['is_active']