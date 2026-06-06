#!/usr/bin/env python
"""
Script to populate the database with sample data.
Run from the backend directory: python populate_db.py
"""
import os
import sys
import django
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from factory import Faker, Iterator, LazyAttribute, LazyFunction, SubFactory
import factory
from ideaboard.models import Idea, Tag, Comments, Likes

User = get_user_model()

# Import existing factories
from core.factories import UserFactory, TagFactory, IdeaFactory

# We'll create our own factory for Comments to avoid circular imports
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comments
    content = Faker('sentence', nb_words=10)
    author = SubFactory(UserFactory)
    idea = SubFactory(IdeaFactory)
    created_at = Faker('date_time_this_decade')

def clear_data():
    """Clear existing data (except superusers and service tables)."""
    print("Clearing existing data...")
    Likes.objects.all().delete()
    Comments.objects.all().delete()
    Idea.objects.all().delete()
    Tag.objects.all().delete()
    # Keep superusers? We'll delete all non-superuser users.
    User.objects.filter(is_superuser=False).delete()
    print("Data cleared.")

def create_users(num_users=10):
    print(f"Creating {num_users} users...")
    users = UserFactory.create_batch(num_users)
    # Ensure at least one superuser exists
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        print("Created superuser: admin")
    return list(User.objects.all())

def create_tags(num_tags=20):
    print(f"Creating {num_tags} tags...")
    tags = TagFactory.create_batch(num_tags)
    return list(Tag.objects.all())

def create_ideas(users, tags, ideas_per_user=5):
    print(f"Creating ideas...")
    ideas = []
    for user in users:
        num_ideas = random.randint(0, ideas_per_user)
        for _ in range(num_ideas):
            idea = IdeaFactory(author=user)
            # Assign random tags
            if tags:
                idea.tags.set(random.sample(tags, k=min(len(tags), random.randint(0, 3))))
            ideas.append(idea)
    return list(Idea.objects.all())

def create_comments(users, ideas, comments_per_idea=5):
    print(f"Creating comments...")
    for idea in ideas:
        num_comments = random.randint(0, comments_per_idea)
        for _ in range(num_comments):
            CommentFactory(idea=idea, author=random.choice(users))

def create_likes(users, ideas, likes_per_idea=10):
    print(f"Creating likes...")
    for idea in ideas:
        # Ensure we don't exceed the number of users
        max_likes = min(len(users), likes_per_idea)
        num_likes = random.randint(0, max_likes)
        # Select random users who haven't liked this idea yet
        potential_likers = random.sample(users, k=len(users))
        for user in potential_likers[:num_likes]:
            Likes.objects.get_or_create(user=user, idea=idea)

def update_idea_counts():
    print("Updating idea counts...")
    for idea in Idea.objects.all():
        idea.likes_count = idea.likes.count()
        idea.comments_count = idea.comments.count()
        idea.save(update_fields=['likes_count', 'comments_count'])
    print("Idea counts updated.")

def main():
    print("Starting database population...")
    clear_data()

    users = create_users(num_users=15)
    tags = create_tags(num_tags=15)
    ideas = create_ideas(users, tags, ideas_per_user=8)
    create_comments(users, ideas, comments_per_idea=6)
    create_likes(users, ideas, likes_per_idea=12)
    update_idea_counts()

    print("Population complete!")
    print(f"Users: {User.objects.count()}")
    print(f"Tags: {Tag.objects.count()}")
    print(f"Ideas: {Idea.objects.count()}")
    print(f"Comments: {Comments.objects.count()}")
    print(f"Likes: {Likes.objects.count()}")

if __name__ == '__main__':
    main()
