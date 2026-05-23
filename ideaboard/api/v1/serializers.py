
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
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

class Registration(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                      required=True, 
                                      validators=[validate_password],
                                      style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True,
                                              required=True,
                                              style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        return user