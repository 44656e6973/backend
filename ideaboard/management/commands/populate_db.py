import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# В README модели указаны как Comments и Likes, но стандарт Django — единственное число.
# Пробуем импортировать оба варианта, чтобы скрипт не упал.
try:
    from ideaboard.models import Idea, Tag, Comment, Like
except ImportError:
    from ideaboard.models import Idea, Tag, Comments as Comment, Likes as Like

User = get_user_model()

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными (пользователи, идеи, теги, комментарии, лайки)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Удалить все идеи, теги, комментарии и лайки перед заполнением',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка базы данных...')
            Like.objects.all().delete()
            Comment.objects.all().delete()
            Idea.objects.all().delete()
            Tag.objects.all().delete()
            # Пользователей не удаляем, чтобы случайно не снести админа

        # 1. Теги
        self.stdout.write('Создание тегов...')
        tag_names = ['startup', 'design', 'tech', 'business', 'education', 'health', 'gaming', 'ai', 'web3', 'mobile']
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
        
        # 2. Пользователи
        self.stdout.write('Создание пользователей...')
        users = []
        for i in range(10):
            username = f'user_{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'avatar_URL': f'https://i.pravatar.cc/150?img={i}'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
            
        # 3. Идеи
        self.stdout.write('Создание идей...')
        ideas = []
        for i in range(20):
            title = f'Идея номер {i+1}'
            idea, created = Idea.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'Подробное описание идеи номер {i+1}. ' * 5,
                    'status': random.choice(['open', 'closed']),
                    'cover_image_URL': f'https://picsum.photos/seed/idea{i}/800/400',
                    'author': random.choice(users)
                }
            )
            if created:
                # Привязываем от 1 до 3 случайных тегов
                idea.tags.set(random.sample(tags, random.randint(1, 3)))
            ideas.append(idea)
            
        # 4. Комментарии
        self.stdout.write('Создание комментариев...')
        for i in range(50):
            Comment.objects.create(
                content=f'Отличная идея! Полностью согласен с автором (комментарий #{i+1}).',
                author=random.choice(users),
                idea=random.choice(ideas)
            )
            
        # 5. Лайки
        self.stdout.write('Создание лайков...')
        for idea in ideas:
            # Случайное количество пользователей лайкает идею
            likers = random.sample(users, random.randint(0, len(users)))
            for user in likers:
                Like.objects.get_or_create(user=user, idea=idea)
                
        # 6. Синхронизация счетчиков
        # Так как у вас счетчики обновляются через Celery, при прямом создании 
        # объектов в БД поля likes_count и comments_count могут не обновиться.
        # Этот блок принудительно пересчитает их, если они являются полями модели.
        self.stdout.write('Синхронизация счетчиков лайков и комментариев...')
        for idea in ideas:
            try:
                idea.likes_count = Like.objects.filter(idea=idea).count()
                idea.comments_count = Comment.objects.filter(idea=idea).count()
                idea.save(update_fields=['likes_count', 'comments_count'])
            except Exception:
                # Если полей нет (например, они вычисляются динамически через property)
                pass
                
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))