import pytest
from users.models import User

@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword123')
        assert user.email == 'testuser@example.com'
        assert user.check_password('testpassword123')
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='admin@example.com', password='adminpassword123')
        assert superuser.email == 'admin@example.com'
        assert superuser.check_password('adminpassword123')
        assert superuser.is_staff
        assert superuser.is_superuser