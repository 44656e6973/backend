from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IdeaViewSet, RegistrationView, TagView

router = DefaultRouter()
router.register(r'ideas', IdeaViewSet, basename='idea')
router.register(r'tags', TagView, basename='tag' )


urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegistrationView.as_view(), name='register'),
]