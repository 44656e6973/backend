from django.db import migrations


DEFAULT_TAGS = [
    'python',
    'django',
    'frontend',
    'backend',
    'javascript',
    'typescript',
    'react',
    'vue',
    'angular',
    'node.js',
    'fastapi',
    'flask',
    'android',
    'ios',
    'mobile',
    'cross-platform',
    'machine learning',
    'data science',
    'data engineering',
    'data visualization',
    'devops',
    'docker',
    'kubernetes',
    'ci/cd',
    'microservices',
    'api',
    'rest api',
    'graphql',
    'postgresql',
    'mysql',
    'mongodb',
    'redis',
    'game development',
    'blockchain',
    'cybersecurity',
    'cloud computing',
    'serverless',
    'monitoring',
    'observability',
    'artificial intelligence',
    'generative ai',
    'ai agents',
    'llm',
    'virtual reality',
    'augmented reality',
    'internet of things',
    'iot',
    'big data',
    'analytics',
    'automation',
    'robotics',
    'natural language processing',
    'nlp',
    'computer vision',
    'deep learning',
    'neural networks',
    'quantum computing',
    'testing',
    'qa automation',
    'ui/ux',
    'accessibility',
    'performance',
    'open source',
    'startup',
    'saas',
    'fintech',
    'edtech',
    'healthtech',
    'e-commerce',
]


def add_default_tags(apps, schema_editor):
    Tag = apps.get_model('ideaboard', 'Tag')
    Tag.objects.bulk_create(
        [Tag(name=tag.lower().strip()) for tag in DEFAULT_TAGS],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('ideaboard', '0006_remove_default_tags'),
    ]

    operations = [
        migrations.RunPython(add_default_tags, reverse_code=migrations.RunPython.noop),
    ]
