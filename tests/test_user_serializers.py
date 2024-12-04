import pytest
from users.models import User
from users.serializers import UserSerializer

@pytest.mark.django_db
class TestUserSerializer:

    def test_create_user(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
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
        user = User.objects.create_user(email='testuser@example.com', password='testpassword123')
        data = {
            'email': 'updateduser@example.com',
            'password': 'newpassword123',
            'is_active': False,
            'timezone': 'Europe/London'
        }
        serializer = UserSerializer(user, data=data)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.email == data['email']
        assert updated_user.check_password(data['password'])
        assert updated_user.is_active == data['is_active']