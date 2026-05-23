import factory
from django.contrib.auth.hashers import make_password
from ideaboard.models import Idea, Comments, Likes, Tag, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.LazyFunction(lambda: make_password('testpassafsd123'))
    avatar_URL = factory.Faker('image_url')
    created_at = factory.Faker('date_time_this_decade')

class TagFactory(factory.django.DjangoModelFactory):  
    class Meta:
        model = Tag
    name = factory.Faker('word')

class IdeaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Idea
    title = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    status = factory.Iterator(['open', 'in_progress', 'closed'])
    created_at = factory.Faker('date_time_this_decade')
    updated_at = factory.Faker('date_time_this_decade')
    cover_imgage_URL = factory.Faker('image_url')
    author = factory.SubFactory(UserFactory)
    
  
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.tags.set(extracted)