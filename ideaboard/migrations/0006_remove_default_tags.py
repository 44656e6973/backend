from django.db import migrations


DEFAULT_TAGS = [
    'python',
    'django',
    'frontend',
    'backend',
    'android',
    'ios',
    'machine learning',
    'data science',
    'devops',
    'game development',
    'blockchain',
    'cybersecurity',
    'cloud computing',
    'artificial intelligence',
    'virtual reality',
    'augmented reality',
    'internet of things',
    'big data',
    'analytics',
    'automation',
    'robotics',
    'natural language processing',
    'computer vision',
    'deep learning',
    'neural networks',
    'quantum computing',
]


def remove_default_tags(apps, schema_editor):
    Tag = apps.get_model('ideaboard', 'Tag')
    Tag.objects.filter(name__in=DEFAULT_TAGS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ideaboard', '0005_idea_counters'),
    ]

    operations = [
        migrations.RunPython(remove_default_tags, reverse_code=migrations.RunPython.noop),
    ]
