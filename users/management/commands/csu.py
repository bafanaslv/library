from django.core.management import BaseCommand

from users.models import Users


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = Users.objects.create(email="ivc@yandex.ru")
        users.set_password("123qwe")
        users.is_staff = True
        users.is_active = True
        users.is_superuser = True
        users.save()
