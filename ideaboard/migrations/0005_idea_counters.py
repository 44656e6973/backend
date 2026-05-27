from django.db import migrations, models
from django.db.models import Count


def fill_idea_counters(apps, schema_editor):
    Idea = apps.get_model('ideaboard', 'Idea')
    for idea in Idea.objects.annotate(
        current_likes_count=Count('likes', distinct=True),
        current_comments_count=Count('comments', distinct=True),
    ):
        idea.likes_count = idea.current_likes_count
        idea.comments_count = idea.current_comments_count
        idea.save(update_fields=['likes_count', 'comments_count'])


class Migration(migrations.Migration):

    dependencies = [
        ('ideaboard', '0004_rename_cover_imgage_url_idea_cover_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='likes_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='idea',
            name='comments_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(fill_idea_counters, migrations.RunPython.noop),
    ]
