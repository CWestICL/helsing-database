from rest_framework import serializers
from .models import Monster
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    entries = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Monster.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "entries"]


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(label="Password", write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = "Access denied: wrong username or password."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

    class Meta:
        model = User
        fields = ("username", "password")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class MonsterSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Monster
        fields = ["id", "name", "description", "author"]
        read_only_fields = ["id", "author"]

    def create(self, validated_data):
        user = self.context["request"].user
        monster = Monster.objects.create(author=user, **validated_data)
        return monster
