from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from library.models import Books, Lending
from users.models import Users


@shared_task
def send_mail_update_course(course_id):
    """Функция отправки уведомлений при обновлении курса"""
    # Полученаем подписчиков
    books = Lending.objects.all()
    if books:
        for book in books:
            to_email = book.user.email
            subject = "Обновления материалов курса"
            message = "Курс обновлен"
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[to_email],
                from_email=EMAIL_HOST_USER,
                fail_silently=True,
            )


@shared_task
def check_login():
    """Проверяет и деактивирует пользователей, которые не заходили в систему в течении 30 дней."""
    users = Users.objects.filter(
        last_login__lte=timezone.now() - timedelta(days=30), is_active=True
    )
    for user in users:
        # обходим суперпользователя
        if not user.is_superuser:
            user.is_active = False
            user.save()
