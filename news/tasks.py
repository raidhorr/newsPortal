from celery import shared_task
from .models import Post, User
from django.core.mail import send_mail


@shared_task
def email_article(pk):
    author = Post.objects.get(pk=pk).author
    mail_list = [rec['email'] for rec in User.objects.all.values('email')]
    print(mail_list)

    # send_mail(
    #     subject=f'{author} разместил новое сообщение',
    #     message=f'{Post.objects.get(pk=pk).text}',
    #     from_email='raidhorr@gmail.com',
    #     recipient_list=['tehotdel@itcprof.com']
    # )
