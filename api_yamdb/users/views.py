from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    mixins,
    permissions,
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .functions import sending_confirmation_code
from .models import User
from .serializers import (
    SignUpSerializer,
    UserSerializer,
    TokenSerializer
)
from .permissions import IsAthorModeraterAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAthorModeraterAdmin,)
    filter_backends = (filters.SearchFilter)
    search_fields = ('username',)


class SignUpViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny)

    def create(self, request):
        serialezer = SignUpSerializer(data=request.data)
        serialezer.is_valid(raise_exception=True)
        user, create = User.objects.get_or_create(**serialezer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        sending_confirmation_code(
            email=user.email,
            confirmation_code=confirmation_code
        )
        return Response(serialezer.data, status=status.HTTP_200_OK)


class TokenViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            raise Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
