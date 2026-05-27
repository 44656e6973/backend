from celery import shared_task
from django.db import DatabaseError
from django_redis import get_redis_connection
from redis.exceptions import RedisError

from ideaboard.counters import (
    apply_idea_counter_deltas,
    iter_dirty_idea_ids,
    pop_pending_idea_deltas,
    restore_pending_idea_deltas,
)


@shared_task(
    bind=True,
    autoretry_for=(DatabaseError, RedisError),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5},
)
def flush_idea_counter_deltas(self, batch_size=500):
    redis = get_redis_connection('default')
    flushed = 0

    for idea_id in iter_dirty_idea_ids(redis, batch_size=batch_size):
        likes_delta, comments_delta = pop_pending_idea_deltas(redis, idea_id)
        if not likes_delta and not comments_delta:
            continue

        try:
            apply_idea_counter_deltas(idea_id, likes_delta, comments_delta)
        except DatabaseError:
            restore_pending_idea_deltas(
                redis,
                idea_id,
                likes_delta=likes_delta,
                comments_delta=comments_delta,
            )
            raise

        flushed += 1

    return {'flushed_ideas': flushed}
