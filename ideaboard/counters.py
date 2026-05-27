from django.db.models import F, Value
from django.db.models.functions import Greatest
from django_redis import get_redis_connection
from redis.exceptions import RedisError

from ideaboard.models import Idea


DIRTY_IDEAS_KEY = 'ideaboard:idea_counters:dirty'
LIKES_DELTA_KEY = 'ideaboard:idea_counters:{idea_id}:likes_delta'
COMMENTS_DELTA_KEY = 'ideaboard:idea_counters:{idea_id}:comments_delta'

POP_DELTAS_SCRIPT = """
local likes_delta = tonumber(redis.call('GET', KEYS[1]) or '0')
local comments_delta = tonumber(redis.call('GET', KEYS[2]) or '0')
redis.call('DEL', KEYS[1])
redis.call('DEL', KEYS[2])
redis.call('SREM', KEYS[3], ARGV[1])
return {likes_delta, comments_delta}
"""


def _likes_key(idea_id):
    return LIKES_DELTA_KEY.format(idea_id=idea_id)


def _comments_key(idea_id):
    return COMMENTS_DELTA_KEY.format(idea_id=idea_id)


def increment_idea_counter(idea_id, likes_delta=0, comments_delta=0):
    if not likes_delta and not comments_delta:
        return

    try:
        redis = get_redis_connection('default')
        pipeline = redis.pipeline()
        if likes_delta:
            pipeline.incrby(_likes_key(idea_id), likes_delta)
        if comments_delta:
            pipeline.incrby(_comments_key(idea_id), comments_delta)
        pipeline.sadd(DIRTY_IDEAS_KEY, idea_id)
        pipeline.execute()
    except RedisError:
        apply_idea_counter_deltas(idea_id, likes_delta, comments_delta)


def apply_idea_counter_deltas(idea_id, likes_delta=0, comments_delta=0):
    updates = {}
    if likes_delta:
        updates['likes_count'] = Greatest(
            F('likes_count') + Value(likes_delta),
            Value(0),
        )
    if comments_delta:
        updates['comments_count'] = Greatest(
            F('comments_count') + Value(comments_delta),
            Value(0),
        )

    if not updates:
        return 0
    return Idea.objects.filter(id=idea_id).update(**updates)


def get_pending_idea_deltas(idea_id):
    try:
        redis = get_redis_connection('default')
        likes_delta, comments_delta = redis.mget(
            _likes_key(idea_id),
            _comments_key(idea_id),
        )
    except RedisError:
        return 0, 0

    return int(likes_delta or 0), int(comments_delta or 0)


def get_current_idea_counts(idea):
    likes_delta, comments_delta = get_pending_idea_deltas(idea.id)
    return {
        'likes_count': max(idea.likes_count + likes_delta, 0),
        'comments_count': max(idea.comments_count + comments_delta, 0),
    }


def pop_pending_idea_deltas(redis, idea_id):
    likes_delta, comments_delta = redis.eval(
        POP_DELTAS_SCRIPT,
        3,
        _likes_key(idea_id),
        _comments_key(idea_id),
        DIRTY_IDEAS_KEY,
        str(idea_id),
    )
    return int(likes_delta), int(comments_delta)


def restore_pending_idea_deltas(redis, idea_id, likes_delta=0, comments_delta=0):
    pipeline = redis.pipeline()
    if likes_delta:
        pipeline.incrby(_likes_key(idea_id), likes_delta)
    if comments_delta:
        pipeline.incrby(_comments_key(idea_id), comments_delta)
    pipeline.sadd(DIRTY_IDEAS_KEY, idea_id)
    pipeline.execute()


def iter_dirty_idea_ids(redis, batch_size=500):
    yielded = 0
    for idea_id in redis.sscan_iter(DIRTY_IDEAS_KEY, count=batch_size):
        if isinstance(idea_id, bytes):
            idea_id = idea_id.decode()
        yield idea_id
        yielded += 1
        if yielded >= batch_size:
            break
