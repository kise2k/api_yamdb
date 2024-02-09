from rest_framework import (
    filters,
    viewsets,
    permissions,
)
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response


from api.serializers import (
    SignUpSerializer,
    UserSerializer,
    TokenSerializer
)

from api.permission import (
    IsAdmin,
)
from .models import User


class SignUpView(APIView):

    allowed_methods = ['POST']

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)


class TokenView(APIView):

    allowed_methods = ['POST']

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = 'username'

    @action(
        detail=False, methods=['get'],
        url_path='me', url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        return Response(UserSerializer(request.user).data)

    @get_me_data.mapping.patch
    def update_me_data(self, request):
        serializer = UserSerializer(
            request.user, data=request.data,
            partial=True, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)
