import json

from django.core.management import BaseCommand
from django.db import connection

from users.models import Payments


class Command(BaseCommand):

    @staticmethod
    def json_read_payments():
        with open("payments.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def handle(self, *args, **options):

        payments_for_create = []
        payments_sequence = 1
        self.clean_database()
        self.reset_sequences_payments(payments_sequence)

        for payments in Command.json_read_payments():
            payments_for_create.append(
                Payments(
                    payments["pk"],
                    payments["fields"]["user"],
                    payments["fields"]["payment_date"],
                    payments["fields"]["paid_course"],
                    payments["fields"]["paid_lesson"],
                    payments["fields"]["amount"],
                    payments["fields"]["payment_method"],
                )
            )
        Payments.objects.bulk_create(payments_for_create)
        self.reset_sequences_payments(len(payments_for_create))

    @staticmethod
    def reset_sequences_payments(payments_sequence):
        """Сихронизируем автоинкрементные значения таблицы продукты"""
        with connection.cursor() as cursor:
            cursor.execute(
                f"ALTER SEQUENCE users_payments_id_seq RESTART WITH {payments_sequence};"
            )

    @staticmethod
    def clean_database():
        """Очищаем базу данных"""
        Payments.objects.all().delete()
