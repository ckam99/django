import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
from base.tasks.tests import great, say_hello

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.conf.enable_utc = False
app.conf.update(timezone=settings.TIME_ZONE)
app.config_from_object('django.conf:settings', namespace='CELERY')


# app.conf.beat_schedule = {
#     'say-hello-every-10-seconds': {
#         'task': 'base.tasks.tests.say_hello',
#         'schedule': timedelta(seconds=10),
#         # 'schedule': crontab(minute='*/1'),
#     },
#     'great-5-seconds': {
#         'task': 'base.tasks.tests.great',
#         'schedule': timedelta(seconds=5),
#         'args': ('Rebecca')
#     },
#     'say-hello-every-sunday-at': {
#         'task': 'base.tasks.tests.say_hello',
#         'schedule':  crontab(hour=7, minute=30, day_of_week=1),
#     },

# }

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls notify_students every 5 seconds.
    sender.add_periodic_task(5.0, great.s('Rebecca'),
                             name='greating Rebecca', expires=10)

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(10.0, say_hello)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        say_hello.s(),
    )


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
