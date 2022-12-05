from django.contrib.auth.models import User
from .models import Monster
from .serializers import MonsterSerializer, RegisterSerializer, UserSerializer
from rest_framework import status, permissions, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from . import serializers


@api_view(["POST"])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        _created, token = AuthToken.objects.create(user)
        return Response(
            {"user_info": {"id": user.id, "username": user.username}, "token": token}
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        _created, token = AuthToken.objects.create(user)
        return Response(
            {"user_info": {"id": user.id, "username": user.username}, "token": token}
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def monster_list(request, format=None):

    user = request.user
    print(request.data)
    if not user.is_authenticated:
        return Response(
            {"message": "Log in to see this data"}, status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "GET":
        if user.is_superuser:
            monsters = Monster.objects.all()
        else:
            monsters = Monster.objects.filter(author=user)

        serializer = MonsterSerializer(monsters, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = MonsterSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def monster_indiv(request, id, format=None):

    user = request.user
    print(request.data)
    if not user.is_authenticated:
        return Response(
            {"message": "Log in to see this data"}, status=status.HTTP_403_FORBIDDEN
        )

    try:
        monster = Monster.objects.get(pk=id)
    except Monster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(monster.author)
    print(user)
    print(user.is_superuser)

    if not monster.author == user and not user.is_superuser:
        return Response(
            {"message": "You do not have permission for this entry"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "GET":
        serializer = MonsterSerializer(monster)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = MonsterSerializer(monster, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        monster.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def get_user(request):
    user = request.user
    print(user)
    if user.is_authenticated:
        return Response(
            {
                "user info": {"user id": user.id, "username": user.username},
            }
        )
    return Response(status=status.HTTP_403_FORBIDDEN)
