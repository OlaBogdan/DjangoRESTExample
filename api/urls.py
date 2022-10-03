from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'actors', views.ActorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
