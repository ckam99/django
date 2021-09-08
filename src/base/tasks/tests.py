from celery import shared_task


@shared_task(bind=True)
def say_hello(self):
    print('Hello everybody!')
    return 'Done'


@shared_task(bind=True)
def great(self, name):
    print('Hi {}!'.format(name))
    return 'Done'
