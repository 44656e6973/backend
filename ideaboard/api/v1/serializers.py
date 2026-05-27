from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from ideaboard.models import User, Idea, Comments, Likes, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar_URL', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id'] 

    def validate_name(self, value): 
        if not value.strip():
            raise serializers.ValidationError("Tag name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("Tag name cannot exceed 50 characters.")
        return value


class IdeaSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Idea
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at', 'cover_image_URL', 'author', 'tags']
        read_only_fields = ['author', 'created_at', 'updated_at', 'id']  

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 100:
            raise serializers.ValidationError("Title cannot exceed 100 characters.")
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        if len(value) > 2000:
            raise serializers.ValidationError("Description cannot exceed 2000 characters.")
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return value

    def validate_status(self, value):
        if value not in ['open', 'closed']:
            raise serializers.ValidationError("Status must be one of: open, closed.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'content', 'created_at', 'author', 'idea']
        read_only_fields = ['author', 'created_at', 'idea', 'id']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['idea_id'] = self.context.get('view', {}).kwargs.get('idea_pk')
        return super().create(validated_data)

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        if len(value) > 500:
            raise serializers.ValidationError("Content cannot exceed 500 characters.")
        return value


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Likes
        fields = ['id', 'user', 'idea']
        read_only_fields = ['user', 'idea', 'id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['idea_id'] = self.context.get('view', {}).kwargs.get('idea_pk')
        return super().create(validated_data)

    def validate(self, attrs):
        request = self.context.get('request')
        view = self.context.get('view')
        if not request or not view:
            return attrs
        user = request.user
        idea_pk = view.kwargs.get('idea_pk')
        if idea_pk and Likes.objects.filter(user=user, idea_id=idea_pk).exists():
            raise serializers.ValidationError("You have already liked this idea.")
        return attrs


class Registration(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value