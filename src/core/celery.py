import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
# app.conf.enable_utc = False
# app.conf.update(timezone=settings.TIME_ZONE)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):

#     sender.add_periodic_task(5.0, add.s(41, 8), name='add every 10')

#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s(
#         'hello'), name='say-hello-every-10-seconds')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)

#     sender.add_periodic_task(crontab(minute='*/1'), say_hello.s())

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
