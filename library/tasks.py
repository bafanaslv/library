from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from library.models import Lending
from users.models import Users


@shared_task
def send_mail_return_books():
    """Функция отправки уведомлений читателям о небходимости возвата книг."""
    # Получаем список книг не возвращненых читателями.
    books_for_return = Lending.objects.filter(date_return=None)
    if books_for_return:
        for book_for_return in books_for_return:
            to_email = book_for_return.user.email
            subject = "Возврат книги"
            message = f"Вы должны вернуть книгу {book_for_return.book.name}"
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[to_email],
                from_email=EMAIL_HOST_USER,
                fail_silently=True,
            )

#
# @shared_task
# def check_login():
#     """Проверяет и деактивирует пользователей, которые не заходили в систему в течении 30 дней."""
#     users = Users.objects.filter(
#         last_login__lte=timezone.now() - timedelta(days=30), is_active=True
#     )
#     for user in users:
#         # обходим суперпользователя
#         if not user.is_superuser:
#             user.is_active = False
#             user.save()
