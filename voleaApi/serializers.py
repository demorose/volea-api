from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from .models import Item, Profile, Category

class SimpleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('pk', 'birthday', 'avatar')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        read_only_fields = ['id']
        fields = ['id', 'name', 'owner']

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Item
        read_only_fields = ['id']
        fields = ['id', 'name', 'owner', 'checker']
    def get_validation_exclusions(self):
        exclusions = super(ItemSerializer, self).get_validation_exclusions()
        return exclusions + ['owner']

class VoleaRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    birthday = serializers.DateField()
    avatar = serializers.URLField(required=False)

    def custom_signup(self, request, user):
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.save()
        avatar = None
        if('avatar' in request.data):
            avatar = request.data['avatar']
        Profile.objects.create(user = user, birthday = request.data['birthday'], avatar = avatar)

class VoleaUserDetailsSerializer(serializers.ModelSerializer):
    profile = SimpleProfileSerializer()
    
    class Meta:
        model = User
        fields = ['pk', 'username', 'last_name', 'first_name', 'email', 'profile']
        read_only_fields = ['email']
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.save()

        profile.birthday = profile_data.get('birthday', profile.birthday)
        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.save()

        return instance
