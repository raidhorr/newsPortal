from celery import shared_task
from .models import Post, User
from django.core.mail import send_mail
from datetime import datetime, timedelta


@shared_task
def email_article(pk):
    author = Post.objects.get(pk=pk).author
    mail_list = [usr.email for usr in User.objects.all() if usr.email]

    send_mail(
        subject=f'{author} разместил новое сообщение',
        message=f'{Post.objects.get(pk=pk).text}',
        from_email='raidhorr@gmail.com',
        recipient_list=mail_list
    )


@shared_task
def review():
    mail_list = [usr.email for usr in User.objects.all() if usr.email]
    message = ''
    for post in Post.objects.all():
        if post.time_in > datetime.now()-timedelta(days=7):
            message += f'{post.preview()}\n'
    send_mail(
        subject=f'Обзор сообщений за  неделю',
        message=message,
        from_email='raidhorr@gmail.com',
        recipient_list=mail_list
    )
