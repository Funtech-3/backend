from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(viewsets.ViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, pk=None):
        """Безопасный метод получения информации о юзере."""

        user = get_object_or_404(User, yandex_id=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # Cкорее всего никогда использоватсья не будет.

    def create(self, request):
        """Метод создания или получения юзера."""
        yandex_id = request.data.get("id")
        if yandex_id:
            user = User.objects.get(yandex_id=yandex_id)
            if user:
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            response_data = {
                "access_token": access_token,
                "user": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """метод обновления данных о юзере."""

        user = get_object_or_404(User, yandex_id=pk)
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
