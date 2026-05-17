import factory
from django.contrib.auth import get_user_model
from ideaboard.models import Idea, Comments, Likes, Tag, User

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpassafsd123')
    avatar_URL = factory.Faker('image_url')
    created_at = factory.Faker('date_time_this_decade')

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
    tags = factory.RelatedFactoryList('ideaboard.api.v1.factories.TagFactory', factory_related_name='idea', size=3)