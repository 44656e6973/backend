from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ideaboard.models import Idea, Tag, Comments, Likes
from .serializers import IdeaSerializer, Registration, UserSerializer, TagSerializer, CommentSerializer, LikeSerializer

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.select_related("author").prefetch_related("tags").all
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    