from datetime import datetime, timedelta
import pytz

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from config.settings import EMAIL_HOST_USER
from library.models import Lending
from library.services import telegram_message


@shared_task
def send_mail_return_books():
    """Функция отправки уведомлений читателям о небходимости возвата книг."""
    # Получаем список книг не возвращненых читателями.
    timezone.activate(pytz.timezone(settings.CELERY_TIMEZONE))
    zone = pytz.timezone(settings.CELERY_TIMEZONE)
    today = datetime.now(zone).date()  # текущее дата_время

    books_for_return = Lending.objects.filter(date_event=None)
    if books_for_return:
        message = ''
        for book_for_return in books_for_return:
            if today > book_for_return.date_lending + timedelta(days=10):
                message = f"Вы должны немедленно вернуть книгу {book_for_return.book.name}"
            elif today == book_for_return.date_lending + timedelta(days=10):
                message = f"Вы сегодня должны вернуть книгу {book_for_return.book.name}"
            else:
                if today == book_for_return.date_lending + timedelta(days=7):
                    message = f"Вы должны вернуть книгу {book_for_return.book.name} {book_for_return.date_lending + timedelta(days=10)}"

            if message:
                user_tg = book_for_return.user.tg_chat_id  # telegram chat bott id
                if user_tg:
                    telegram_message(user_tg, message)

                to_email = book_for_return.user.email
                subject = "Возврат книги"
                send_mail(
                    subject=subject,
                    message=message,
                    recipient_list=[to_email],
                    from_email=EMAIL_HOST_USER,
                    fail_silently=True,
                )
