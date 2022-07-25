from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True)
def task_func(self, message, title, receiver):
    send_mail(
        title,
        message,
        'bhatttest852@gmail.com',
        receiver,
        fail_silently=False,
    )
    return 'task_Done'
