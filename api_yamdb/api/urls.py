from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    TitleViewSet,
    ReviewsViewSet
)
from users.views import UserViewSet, TokenView, SignUpView

router_ver_1 = DefaultRouter()

router_ver_1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_ver_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_ver_1.register(r'categories', CategoriesViewSet, basename='categories')
router_ver_1.register(r'genres', GenresViewSet, basename='genres')
router_ver_1.register(r'titles', TitleViewSet, basename='titles')
router_ver_1.register(r'users', UserViewSet, basename='user')


auth_urls = [
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'token/',
        TokenView.as_view(),
        name='token'
    )
]


urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_ver_1.urls))
]
