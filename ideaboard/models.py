from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar_URL = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_imgage_URL = models.URLField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    tags = models.ManyToManyField(Tag, related_name='ideas', blank=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.idea.title}"
    
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'idea'],
                name='unique_user_idea_like'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'idea']),
        ]

    

