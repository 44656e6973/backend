import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

try:
    from ideaboard.models import Idea, Tag, Comment, Like
except ImportError:
    from ideaboard.models import Idea, Tag, Comments as Comment, Likes as Like

User = get_user_model()

class Command(BaseCommand):
    help = 'Заполняет базу данных реалистичными тестовыми данными'

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

        # Реалистичные теги из IT-сферы
        self.stdout.write('Создание тегов...')
        tag_names = [
            'python', 'django', 'frontend', 'backend', 'android', 'ios',
            'machine learning', 'data science', 'devops', 'game development',
            'blockchain', 'cybersecurity', 'cloud computing', 'artificial intelligence',
            'virtual reality', 'augmented reality', 'internet of things', 'big data',
            'analytics', 'automation', 'robotics', 'natural language processing',
            'computer vision', 'deep learning', 'neural networks', 'quantum computing'
        ]
        tags = {name: Tag.objects.get_or_create(name=name)[0] for name in tag_names}
        
        # Реалистичные пользователи
        self.stdout.write('Создание пользователей...')
        user_data = [
            ('alex_dev', 'alex@techmail.com', 'Alex Developer'),
            ('maria_code', 'maria@devstudio.com', 'Maria Coder'),
            ('john_backend', 'john@backend.io', 'John Smith'),
            ('sarah_frontend', 'sarah@uiux.design', 'Sarah Johnson'),
            ('dmitry_ml', 'dmitry@ai.research', 'Dmitry Petrov'),
            ('anna_mobile', 'anna@mobiledev.app', 'Anna Williams'),
            ('igor_devops', 'igor@cloudops.tech', 'Igor Sokolov'),
            ('emma_data', 'emma@datascience.pro', 'Emma Davis'),
            ('sergey_game', 'sergey@gamedev.studio', 'Sergey Volkov'),
            ('lisa_security', 'lisa@cybersec.net', 'Lisa Chen'),
        ]
        
        users = []
        avatars = [
            'https://i.pravatar.cc/150?img=11',
            'https://i.pravatar.cc/150?img=5',
            'https://i.pravatar.cc/150?img=3',
            'https://i.pravatar.cc/150?img=9',
            'https://i.pravatar.cc/150?img=13',
            'https://i.pravatar.cc/150?img=10',
            'https://i.pravatar.cc/150?img=15',
            'https://i.pravatar.cc/150?img=20',
            'https://i.pravatar.cc/150?img=33',
            'https://i.pravatar.cc/150?img=44',
        ]
        
        for i, (username, email, _) in enumerate(user_data):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'avatar_URL': avatars[i % len(avatars)],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # Реалистичные идеи для IT-проектов
        self.stdout.write('Создание идей...')
        ideas_data = [
            {
                'title': 'Платформа для онлайн-обучения программированию',
                'description': 'Интерактивная платформа с курсами по Python, JavaScript и другим языкам программирования. Включает в себя систему автоматической проверки кода, персонализированный план обучения и проектную работу.',
                'tags': ['python', 'django', 'frontend', 'backend', 'education'],
                'status': 'open'
            },
            {
                'title': 'Мобильное приложение для трекинга здоровья',
                'description': 'Приложение для отслеживания физической активности, питания и сна. Интеграция с фитнес-браслетами, AI-рекомендации по улучшению образа жизни.',
                'tags': ['android', 'ios', 'machine learning', 'data science'],
                'status': 'open'
            },
            {
                'title': 'Система автоматического тестирования веб-приложений',
                'description': 'DevOps инструмент для автоматизации тестирования frontend и backend частей приложения. Поддержка CI/CD пайплайнов.',
                'tags': ['devops', 'automation', 'frontend', 'backend'],
                'status': 'open'
            },
            {
                'title': 'Игра в жанре RPG с открытым миром',
                'description': 'Многопользовательская ролевая игра с процедурной генерацией мира. Использование современных графических технологий и сетевого кода.',
                'tags': ['game development', 'backend', 'cloud computing'],
                'status': 'closed'
            },
            {
                'title': 'Платформа для анализа больших данных',
                'description': 'Облачная платформа для обработки и визуализации больших объемов данных. Поддержка real-time аналитики и машинного обучения.',
                'tags': ['big data', 'analytics', 'cloud computing', 'machine learning'],
                'status': 'open'
            },
            {
                'title': 'Чат-бот с NLP для службы поддержки',
                'description': 'Интеллектуальный чат-бот для автоматизации службы поддержки клиентов. Понимание естественного языка, интеграция с CRM системами.',
                'tags': ['natural language processing', 'artificial intelligence', 'automation', 'backend'],
                'status': 'open'
            },
            {
                'title': 'Система компьютерного зрения для ритейла',
                'description': 'Анализ покупательского поведения в магазинах с помощью камер видеонаблюдения. Распознавание товаров на полках, подсчет посетителей.',
                'tags': ['computer vision', 'deep learning', 'analytics'],
                'status': 'open'
            },
            {
                'title': 'Блокчейн платформа для смарт-контрактов',
                'description': 'Децентрализованная платформа для создания и исполнения смарт-контрактов. Высокая производительность и безопасность.',
                'tags': ['blockchain', 'cybersecurity', 'backend'],
                'status': 'closed'
            },
            {
                'title': 'Приложение дополненной реальности для туризма',
                'description': 'AR-гид по городу с наложением исторической информации на реальные объекты. Оффлайн режим и социальная составляющая.',
                'tags': ['augmented reality', 'android', 'ios', 'frontend'],
                'status': 'open'
            },
            {
                'title': 'Система управления умным домом',
                'description': 'Централизованная платформа для управления IoT устройствами: освещение, отопление, безопасность. Голосовое управление.',
                'tags': ['internet of things', 'automation', 'backend', 'mobile'],
                'status': 'open'
            },
            {
                'title': 'Фреймворк для быстрой разработки REST API',
                'description': 'Легковесный Python фреймворк для создания масштабируемых API с автоматической документацией и валидацией данных.',
                'tags': ['python', 'backend', 'devops', 'cloud computing'],
                'status': 'open'
            },
            {
                'title': 'Платформа для совместной разработки кода',
                'description': 'Online IDE с возможностью совместного редактирования кода в реальном времени. Встроенный чат и видеозвонки.',
                'tags': ['frontend', 'backend', 'cloud computing', 'automation'],
                'status': 'open'
            },
            {
                'title': 'Система обнаружения кибератак',
                'description': 'AI-система для мониторинга сетевого трафика и выявления аномалий. Автоматическое реагирование на угрозы.',
                'tags': ['cybersecurity', 'machine learning', 'big data', 'automation'],
                'status': 'closed'
            },
            {
                'title': 'Генератор кода с помощью нейросетей',
                'description': 'Инструмент для автоматической генерации кода на основе описания функциональности. Поддержка нескольких языков программирования.',
                'tags': ['artificial intelligence', 'neural networks', 'deep learning', 'automation'],
                'status': 'open'
            },
            {
                'title': 'Платформа для обучения нейронных сетей',
                'description': 'Облачная платформа с GPU для тренировки моделей машинного обучения. Готовые шаблоны и визуальный конструктор.',
                'tags': ['machine learning', 'deep learning', 'cloud computing', 'neural networks'],
                'status': 'open'
            },
            {
                'title': 'Система распознавания речи',
                'description': 'API для преобразования речи в текст и обратно. Поддержка множественных языков и диалектов.',
                'tags': ['natural language processing', 'deep learning', 'backend'],
                'status': 'open'
            },
            {
                'title': 'Приложение для VR-тренингов',
                'description': 'Виртуальная реальность для корпоративного обучения: презентации, переговоры, технические навыки.',
                'tags': ['virtual reality', 'frontend', 'game development'],
                'status': 'closed'
            },
            {
                'title': 'Автоматизация развертывания микросервисов',
                'description': 'DevOps платформа для оркестрации контейнеров, автоматического масштабирования и мониторинга.',
                'tags': ['devops', 'cloud computing', 'automation', 'backend'],
                'status': 'open'
            },
            {
                'title': 'Система рекомендаций для e-commerce',
                'description': 'ML-алгоритмы для персонализации контента и товаров. A/B тестирование и аналитика.',
                'tags': ['machine learning', 'data science', 'analytics', 'backend'],
                'status': 'open'
            },
            {
                'title': 'Роботизированная система сортировки',
                'description': 'Промышленные роботы с компьютерным зрением для автоматической сортировки товаров на складе.',
                'tags': ['robotics', 'computer vision', 'automation', 'iot'],
                'status': 'open'
            },
        ]
        
        ideas = []
        cover_images = [
            'https://picsum.photos/seed/tech1/800/400',
            'https://picsum.photos/seed/code2/800/400',
            'https://picsum.photos/seed/ai3/800/400',
            'https://picsum.photos/seed/app4/800/400',
            'https://picsum.photos/seed/data5/800/400',
            'https://picsum.photos/seed/cloud6/800/400',
            'https://picsum.photos/seed/mobile7/800/400',
            'https://picsum.photos/seed/game8/800/400',
            'https://picsum.photos/seed/security9/800/400',
            'https://picsum.photos/seed/vr10/800/400',
        ]
        
        now = timezone.now()
        
        for i, idea_data in enumerate(ideas_data):
            idea, created = Idea.objects.get_or_create(
                title=idea_data['title'],
                defaults={
                    'description': idea_data['description'],
                    'status': idea_data['status'],
                    'cover_image_URL': cover_images[i % len(cover_images)],
                    'author': random.choice(users),
                    'created_at': now - timedelta(days=random.randint(1, 60)),
                }
            )
            
            # Привязываем теги
            idea_tags = [tags[tag_name] for tag_name in idea_data['tags'] if tag_name in tags]
            idea.tags.set(idea_tags)
            
            ideas.append(idea)
            
        # Реалистичные комментарии
        self.stdout.write('Создание комментариев...')
        comments_data = [
            "Отличная идея! Давно искал что-то подобное. Готов помочь с frontend частью.",
            "Звучит перспективно. Есть опыт работы с подобными системами.",
            "Интересный проект! Какие технологии планируете использовать?",
            "Можно присоединиться? У меня есть опыт в machine learning.",
            "Хорошая концепция. Как насчет использования микросервисной архитектуры?",
            "Поддерживаю! Это решит много проблем в нашей индустрии.",
            "Есть похожий проект в портфолио. Могу поделиться опытом.",
            "Круто! Когда планируется запуск MVP?",
            "Нужна помощь с backend? Работаю с Django 3 года.",
            "Идея супер! Особенно интересна часть с AI.",
            "Готов протестировать альфа-версию.",
            "Отличный подход к решению проблемы!",
            "Как насчет использования GraphQL вместо REST?",
            "Есть идеи по монетизации проекта?",
            "Можно использовать Kubernetes для оркестрации.",
            "Звучит сложно, но реализуемо. Удачи!",
            "Интересно, как будете решать проблему масштабирования?",
            "Хотелось бы увидеть демо-версию.",
            "Открыт для сотрудничества!",
            "Технически грамотно описано. Респект!",
        ]
        
        for i in range(80):
            Comment.objects.create(
                content=random.choice(comments_data),
                author=random.choice(users),
                idea=random.choice(ideas),
                created_at=now - timedelta(days=random.randint(1, 45))
            )
            
        # Лайки
        self.stdout.write('Создание лайков...')
        for idea in ideas:
            likers = random.sample(users, random.randint(0, min(7, len(users))))
            for user in likers:
                Like.objects.get_or_create(user=user, idea=idea)
                
        # Синхронизация счетчиков
        self.stdout.write('Синхронизация счетчиков...')
        for idea in ideas:
            idea.likes_count = Like.objects.filter(idea=idea).count()
            idea.comments_count = Comment.objects.filter(idea=idea).count()
            idea.save(update_fields=['likes_count', 'comments_count'])
            
        self.stdout.write(self.style.SUCCESS(f'''
✅ База данных успешно заполнена!
   
📊 Статистика:
   - Пользователей: {len(users)}
   - Тегов: {len(tags)}
   - Идей: {len(ideas)}
   - Комментариев: {Comment.objects.count()}
   - Лайков: {Like.objects.count()}

🔑 Данные для входа:
   - Логин: alex_dev, maria_code, john_backend и т.д.
   - Пароль: password123
        '''))