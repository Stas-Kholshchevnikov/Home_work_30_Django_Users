from rest_framework.fields import IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User, Location


class UserSerializer(ModelSerializer):
    class Meta:
        exclude = ['password']
        model = User


class UserListSerializer(ModelSerializer):
    total_ads = IntegerField()

    class Meta:
        exclude = ['password']
        model = User


class UserCreateSerializer(ModelSerializer):
    location = SlugRelatedField(required=False,
                                many=True,
                                slug_field="name",
                                queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user_password = validated_data.pop("password")
        new_user = User.objects.create(**validated_data)
        new_user.set_password(user_password)
        new_user.save()
        for each_loc in self._location:
            loc, created = Location.objects.get_or_create(name=each_loc)
            new_user.location.add(loc)
        return new_user

    class Meta:
        fields = '__all__'
        model = User


class UserUpdateSerializer(ModelSerializer):
    location = SlugRelatedField(required=False,
                                many=True,
                                slug_field="name",
                                queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.location.clear()
        for each_loc in self._location:
            loc, created = Location.objects.get_or_create(name=each_loc)
            user.location.add(loc)
        return user

    class Meta:
        exclude = ['password']
        model = User


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'