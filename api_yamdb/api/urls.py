from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_ver_1 = DefaultRouter()

router_ver_1.register(
    r'titles/(?P<title_id>\d+)',
    ReviewsViewSet,
    basename='reviews'
)
router_ver_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_ver_1.register(r'categories', CategoriesViewSet, basename='categories')
router_ver_1.register(r'genre', GenresViewSet, basename='genres')
router_ver_1.register(r'title', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router_ver_1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
