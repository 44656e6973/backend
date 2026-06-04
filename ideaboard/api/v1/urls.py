from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    IdeaViewSet,
    LikeViewSet,
    LogoutView,
    RegistrationView,
    TagView,
    UserViewSet,
    LoginView,
)

router = DefaultRouter()
router.register(r'ideas', IdeaViewSet, basename='idea')
router.register(r'tags', TagView, basename='tag' )


urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/login', LoginView.as_view()),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('users/me/', UserViewSet.as_view(), name='user-me'),   
    path(
        'ideas/<int:idea_pk>/comments/',
        CommentViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='idea-comments'
    ),
    
    path(
        'ideas/<int:idea_pk>/likes/',
        LikeViewSet.as_view({
            'post': 'toggle_like',
            'delete': 'destroy' 
        }),
        name='idea-likes'
    ),
]
