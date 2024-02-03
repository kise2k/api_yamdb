from django.urls import path, include
from rest_framework import routers

from users.views import (
    UserViewSet,
    SignUpViewSet,
    TokenViewSet,
)


router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')


auth_urls = [
    path(
        'signup/',
        SignUpViewSet.as_view({'post': 'create'}),
        name='signup',
    ),
    path(
        'token/',
        TokenViewSet.as_view({'post': 'create'}),
        name='token',
    )
]


v1_urls = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls)),
]


urlpatterns = [
    path('v1/', include(v1_urls))
]

