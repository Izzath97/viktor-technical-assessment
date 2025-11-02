"""
URL Configuration for Shop API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BookViewSet,
    MusicAlbumViewSet,
    SoftwareLicenseViewSet,
    CartViewSet
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'music-albums', MusicAlbumViewSet, basename='music-album')
router.register(r'software-licenses', SoftwareLicenseViewSet,
                basename='software-license')
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
