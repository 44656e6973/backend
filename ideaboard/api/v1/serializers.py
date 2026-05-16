from django.contrib.auth.models import Group, User
from rest_framework import serializers
from ideaboard.models import User, Idea, Comments, Likes, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar_URL', 'created_at']

class IdeaSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Idea
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at', 'cover_imgage_URL', 'author', 'tags']
        read_only_fields = ['author', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'content', 'created_at', 'author', 'idea']
        read_only_fields = ['author', 'created_at', 'idea']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Likes
        fields = ['id', 'user', 'idea']
        read_only_fields = ['user', 'idea']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']