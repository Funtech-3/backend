from http.client import BAD_REQUEST, CREATED, OK

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import City, NotificationSwitch, Tag
from .permissions import IsAuthenticatedAndOwner
from .serializers import (
    CitiesSerializer,
    CustomUserSerializer,
    InterestsSerializer,
    NotificationSwitchSerializer,
    TagsSerializer,
)

User = get_user_model()


class CustomUserViewSet(ViewSet):
    """Возвращяет экземпляр юзера, создает и изменяет.
    Используется ЯндексID для создания юзера и токена.
    """

    serializer_class = CustomUserSerializer
    pagination_class = None
    permission_classes = (AllowAny,)

    def retrieve(self, request, pk=None):
        """Безопасный метод получения информации о юзере."""

        user = get_object_or_404(User, yandex_id=pk)
        serializer = self.serializer_class(user)
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        response_data = {
            "access_token": access_token,
            "refresh_token": str(refresh_token),
            "user": serializer.data,
        }
        return Response(response_data, status=OK)

    def create(self, request):
        """Метод создания или получения юзера."""

        yandex_id = request.data.get("yandex_id")
        if yandex_id:
            user = User.objects.filter(yandex_id=yandex_id).first()
            if user:
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=OK)
            username = request.data.get("login", None)
            email = request.data.get("default_email", None)
            phone_number = request.data.get("defaulte_phone", {}).get(
                "number", None
            )
            default_avatar_id = request.data.get("default_avatar_id", None)
            avatar_url = (
                f"https://avatars.yandex.net/get-yapic/{default_avatar_id}/"
            )
            user = User(
                yandex_id=yandex_id,
                username=username,
                email=email,
                phone_number=phone_number,
                avatar=avatar_url,
            )
            user.save()
            serializer = self.serializer_class(user)
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            response_data = {
                "access_token": access_token,
                "refresh_token": str(refresh_token),
                "user": serializer.data,
            }
            return Response(response_data, status=CREATED)
        return Response(status=BAD_REQUEST)

    def update(self, request, pk=None):
        """метод обновления данных о юзере."""

        user = get_object_or_404(User, yandex_id=pk)
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=OK)


class NotificationsViewSet(APIView):
    """Представление для уведомлений в личном кабинете юзера."""

    serializer_class = NotificationSwitchSerializer

    def get(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        notifications = get_object_or_404(NotificationSwitch, user_id=user.id)
        serializer = NotificationSwitchSerializer(notifications)
        return Response(serializer.data, status=OK)

    def post(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        notification, created = NotificationSwitch.objects.get_or_create(
            user=user
        )
        if not created:
            return Response(
                {"message": "Уведомления уже созданы"}, status=BAD_REQUEST
            )
        serializer = NotificationSwitchSerializer(
            notification, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=CREATED)
        return Response(serializer.errors, status=BAD_REQUEST)

    def patch(self, request):
        notification = get_object_or_404(
            NotificationSwitch, id=self.request.user.id
        )
        serializer = NotificationSwitchSerializer(
            notification, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=OK)
        return Response(serializer.errors, status=BAD_REQUEST)


class InterestsViewSet(RetrieveUpdateAPIView):
    """Представление для тегов и городов в личном кабинете юзера."""

    serializer_class = InterestsSerializer
    permission_classes = (IsAuthenticatedAndOwner,)
    pagination_class = None

    def get_object(self):
        return self.request.user


class TagsViewSet(ListAPIView):
    """Представление для тегов для главной страницы."""

    serializer_class = TagsSerializer
    queryset = Tag.objects.all()
    pagination_class = None

    def get_object(self):
        return self.request.user


class CitiesViewSet(ListAPIView):
    """Представление для тегов для главной страницы."""

    serializer_class = CitiesSerializer
    queryset = City.objects.all()
    pagination_class = None

    def get_object(self):
        return self.request.user
