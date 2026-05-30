from rest_framework import viewsets, permissions, generics, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from ideaboard.models import Idea, Tag, Comments, Likes, User
from ideaboard.counters import increment_idea_counter
from .serializers import IdeaSerializer, Registration, UserSerializer, TagSerializer, CommentSerializer, LikeSerializer, LoginSerializer




class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.select_related("author").prefetch_related("tags").all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
class RegistrationView(generics.CreateAPIView):
    serializer_class = Registration
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
class TagView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()  
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def save(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.select_related('author', 'idea').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comments.objects.filter(
            idea_id=self.kwargs['idea_pk']
        ).select_related('author').order_by('-created_at')

    def perform_create(self, serializer):
        comment = serializer.save(
            author=self.request.user,
            idea_id=self.kwargs['idea_pk']
        )
        transaction.on_commit(
            lambda: increment_idea_counter(comment.idea_id, comments_delta=1)
        )

    def perform_destroy(self, instance):
        idea_id = instance.idea_id
        instance.delete()
        transaction.on_commit(
            lambda: increment_idea_counter(idea_id, comments_delta=-1)
        )

class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Likes.objects.filter(idea_id=self.kwargs["idea_pk"])
    
    def create(self, request, *args, **kwargs):
        idea_pk = self.kwargs.get("idea_pk")
        like, created = Likes.objects.get_or_create(user=request.user, idea_id=idea_pk)
        if created:
            transaction.on_commit(
                lambda: increment_idea_counter(idea_pk, likes_delta=1)
            )
            return Response({"status": "liked", "like_id": like.id}, status=status.HTTP_201_CREATED)
        return Response({"status": "already_liked", "like_id": like.id}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='toggle-like', url_name='like-toggle', permission_classes=[permissions.IsAuthenticated])
    def toggle_like(self, request, *args, **kwargs):
        """
        URL: POST /api/v1/ideas/<idea_pk>/likes/toggle/
        """
        idea_pk = self.kwargs.get("idea_pk")
        user = request.user
        
        like, created = Likes.objects.get_or_create(user=user, idea_id=idea_pk)
        
        if not created:
            like.delete()
            transaction.on_commit(
                lambda: increment_idea_counter(idea_pk, likes_delta=-1)
            )
            return Response({"status": "unliked"}, status=status.HTTP_200_OK)
        transaction.on_commit(
            lambda: increment_idea_counter(idea_pk, likes_delta=1)
        )
        return Response({"status": "liked", "like_id": like.id}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        URL: DELETE /api/v1/ideas/<idea_pk>/likes/<like_id>/
        """
        try:
            like = Likes.objects.get(user=request.user, idea_id=self.kwargs['idea_pk'])
            like.delete()
            idea_pk = self.kwargs['idea_pk']
            transaction.on_commit(
                lambda: increment_idea_counter(idea_pk, likes_delta=-1)
            )
            return Response({"status": "unliked"}, status=status.HTTP_200_OK)
        except Likes.DoesNotExist:
            return Response({"detail": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта (для GET/PUT/PATCH) или админу.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return obj == request.user

class UserViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def perform_authentication(self, request):
        return super().perform_authentication(request)
