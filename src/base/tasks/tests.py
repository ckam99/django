from celery import shared_task


@shared_task
def say_hello():
    return 'Hello everybody!'


@shared_task
def great():
    return 'Hi Rebecca'


@shared_task
def test(arg):
    print(arg)


@shared_task
def add(x, y):
    z = x + y
    print(z)
