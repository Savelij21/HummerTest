from django.shortcuts import render
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import viewsets, views
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import User
from .utils import generate_invite_code
from .serializers import UserSerializer

import random
import time


# Для тестов - мб потом в редис
auth_codes = {}


class AuthViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    def phone_auth(self, request):
        phone: str = request.data.get('phone', None)

        if not phone:
            raise ValidationError({'detail': 'Требуется предоставить номер телефона'})

        auth_code = random.randint(1111, 9999)  # мб в редис?
        auth_codes[phone] = auth_code
        time.sleep(2)  # "отправка смс"

        return Response({
            'detail': 'Код подтверждения отправлен на указанный телефон',
            'test_auth_code': auth_code
        }, status=201)

    @action(methods=['POST'], detail=False)
    def code_auth(self, request):
        code: str = request.data.get('code', None)
        phone: str = request.data.get('phone', None)

        if not code or not phone:
            raise ValidationError({'detail': 'Требуется предоставить код подтверждения и телефон'})

        cached_code = auth_codes.get(phone, None)

        if cached_code is None:
            raise ValidationError({'detail': 'Срок действия кода подтверждения истек'})
        elif int(code) != cached_code:
            raise ValidationError({'detail': 'Неверный код подтверждения'})

        # DEV
        del auth_codes[phone]

        if not User.objects.filter(phone=phone).exists():
            new_invite_code = generate_invite_code()
            user: User = User.objects.create(
                phone=phone,
                invite_code=new_invite_code,
                username=f'User_{new_invite_code}'
            )

            return Response({
                'detail': 'Новый пользователь успешно создан и аутентифицирован',
                'user': UserSerializer(user).data,
                'token': Token.objects.create(user=user).key
            }, status=201)

        token, created_at = Token.objects.get_or_create(user=User.objects.get(phone=phone))

        return Response({
            'detail': 'Аутентификация прошла успешно',
            'token': token.key
        }, status=201)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def get_profile(self, request):
        """
        Получение профиля пользователя
        """
        user: User = request.user
        serializer = UserSerializer(user)

        return Response(
            data=serializer.data,
            status=200
        )

    @action(methods=['POST'], detail=False)
    def set_foreign_invite_code(self, request):
        """
        Установка реферальной связи с другим юзером через инвайт-код
        """
        user: User = request.user
        foreign_invite_code: str = request.data.get('foreign_invite_code', None)

        if foreign_invite_code:
            if not User.objects.filter(invite_code=foreign_invite_code).exists():
                raise ValidationError({'detail': 'Неверный инвайт-код'})

            user.foreign_invite_code = foreign_invite_code
            user.save()
            return Response({
                'detail': 'Реферальная связь успешно установлена',
                'user': UserSerializer(user).data
            }, status=201)

        raise ValidationError({'detail': 'Требуется предоставить инвайт-код'})

    @action(methods=['POST'], detail=False)
    @csrf_exempt
    def user_logout(self, request):
        Token.objects.get(user=request.user).delete()
        return Response({'detail': 'Пользователь вышел из аккаунта'}, status=201)


