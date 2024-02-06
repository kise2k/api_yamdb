from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import (
    filters,
    permissions,
    viewsets,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permission import IsAdmin
from .models import User
from .serializers import (
    SignUpSerializer,
    UserSerializer,
    TokenSerializer
)


class SignUpView(APIView):

    allowed_methods = ['POST']

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenView(APIView):

    allowed_methods = ['POST']

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        token = AccessToken.for_user(user)
        return Response({'token': str(token)},
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'

    @action(
        detail=False, methods=['get'],
        url_path='me', url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_me_data.mapping.patch
    def update_me_data(self, request):
        serializer = UserSerializer(
            request.user, data=request.data,
            partial=True, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
