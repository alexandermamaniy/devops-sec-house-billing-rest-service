from rest_framework import serializers
from users.models import User
from buddy_profiles.models import BuddyProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class BuddyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BuddyProfile
        fields = ['id', 'user', 'full_name', 'picture_url', 'is_active']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        buddy_profile = BuddyProfile.objects.create(user=user, **validated_data)
        return buddy_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.picture_url = validated_data.get('picture_url', instance.picture_url)
        instance.is_active = validated_data.get('is_active', user.is_active)
        instance.save()

        user.email = user_data.get('email', user.email)
        if 'password' in user_data:
            user.set_password(user_data['password'])
        user.is_active = user_data.get('is_active', user.is_active)
        user.save()

        return instance

class BuddyMemberOfAGroupRetrieveSerializer(serializers.Serializer):
    members_of_group = BuddyProfileSerializer( many=True)
    admins_of_group = BuddyProfileSerializer(  many=True)