from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Authors, Books, Lending
from users.models import Users


class AuthorsTestCase(APITestCase):
    """Тестирование CRUD авторов."""

    def setUp(self):
        self.user = Users.objects.create(
            email="ivc@yandex.ru",
            password="123qwe",
            is_superuser=True,
        )
        group = Group.objects.create(name="librarian")
        group.user_set.add(self.user)
        self.author = Authors.objects.create(author="Джек Лондон")
        self.client.force_authenticate(user=self.user)

    def test_author_list(self):
        url = reverse("authors-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_retrieve(self):
        url = reverse("authors-detail", args=(self.author.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("author"), self.author.author)

    def test_author_create(self):
        url = reverse("authors-list")
        data = {
            "author": "Марк Твен",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Books.objects.all().count(), 0)

    def test_author_update(self):
        url = reverse("authors-detail", args=(self.author.pk,))
        data = {
            "author": "Марк Твен",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("author"), "Марк Твен")

    def test_author_delete(self):
        url = reverse("authors-detail", args=(self.author.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Books.objects.all().count(), 0)


class BooksTestCase(APITestCase):
    """Тестирование CRUD книг."""

    def setUp(self):
        self.user = Users.objects.create(
            email="ivc@yandex.ru",
            password="123qwe",
            is_superuser=True,
        )
        group = Group.objects.create(name="librarian")
        group.user_set.add(self.user)
        self.author = Authors.objects.create(author="Джек Лондон")
        self.book = Books.objects.create(
            name="Любовь к жизни",
            genre="story",
            barcode="1111111111",
            author=self.author,
        )
        self.client.force_authenticate(user=self.user)

    def test_books_list(self):
        url = reverse("books-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_retrieve(self):
        url = reverse("books-detail", args=(self.book.pk,))
        response = self.client.get(url)
        # print(response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.book.name)

    def test_book_create(self):
        url = reverse("books-list")
        data = {
            "name": "Костер",
            "genre": "story",
            "author": self.author.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Books.objects.all().count(), 2)

    def test_book_update(self):
        url = reverse("books-detail", args=(self.book.pk,))
        data = {
            "name": "Костер",
            "genre": "story",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Костер")

    def test_course_delete(self):
        url = reverse("books-detail", args=(self.book.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Books.objects.all().count(), 0)


class LibraryCreateTestCase(APITestCase):
    """Тестирование работы библиотеки."""

    def setUp(self):
        self.user = Users.objects.create(
            email="ivc@yandex.ru",
            password="123qwe",
            is_superuser=True,
        )
        group = Group.objects.create(name="librarian")
        group.user_set.add(self.user)
        self.author = Authors.objects.create(author="Джек Лондон")
        self.book = Books.objects.create(
            name="Любовь к жизни",
            genre="story",
            barcode="1111111111",
            author=self.author,
        )
        self.lending = Lending.objects.create(
            user=self.user,
            book=self.book,
            operation="arrival",
            arrival_quantity=2,
        )
        self.client.force_authenticate(user=self.user)

    def test_lending_list(self):
        url = reverse("library:lending_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lending_retrieve(self):
        url = reverse("library:lending_retrieve", args=(self.lending.pk,))
        response = self.client.get(url)
        # print(response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("operation"), self.lending.operation)

    def test_lending_create_arrival(self):
        """Тест поступления партии книги в библиотеку."""
        url = reverse("library:lending_create")
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "arrival",
            "arrival_quantity": 1,
        }
        response = self.client.post(url, data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lending.objects.all().count(), 2)

    def test_lending_create_issuance(self):
        """Тест выдачи книги читателю."""
        url = reverse("library:lending_create")
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "arrival",
            "arrival_quantity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "issuance",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lending.objects.all().count(), 3)

    def test_lending_create_return(self):
        """Тест возврата книги в библиотеку."""
        url = reverse("library:lending_create")
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "arrival",
            "arrival_quantity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "issuance",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "return",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lending.objects.all().count(), 4)

    def test_lending_create_loss(self):
        """Тест утери выданной читателю книги."""
        url = reverse("library:lending_create")
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "arrival",
            "arrival_quantity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "issuance",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "loss",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lending.objects.all().count(), 4)

    def test_lending_create_write_off(self):
        """Тест списания физически изношенной книги."""
        url = reverse("library:lending_create")
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "arrival",
            "arrival_quantity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "user": self.user.pk,
            "book": self.book.pk,
            "operation": "write_off",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lending.objects.all().count(), 3)

    class LibraryDeleteTestCase(APITestCase):
        """Тестирование работы библиотеки (отмена операций)."""

        def setUp(self):
            self.user = Users.objects.create(
                email="ivc@yandex.ru",
                password="123qwe",
                is_superuser=True,
            )
            group = Group.objects.create(name="librarian")
            group.user_set.add(self.user)
            self.author = Authors.objects.create(author="Джек Лондон")
            self.book = Books.objects.create(
                name="Любовь к жизни",
                genre="story",
                barcode="1111111111",
                author=self.author,
            )
            self.lending = Lending.objects.create(
                user=self.user,
                book=self.book,
                operation="arrival",
                arrival_quantity=2,
            )
            self.client.force_authenticate(user=self.user)

        def test_lending_arrival_delete(self):
            """Тест отмены поступления партии книги в библиотеку."""
            url = reverse("library:lending_create")
            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "operation": "arrival",
                "arrival_quantity": 1,
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Lending.objects.all().count(), 2)

            url = reverse("library:lending_delete", args=(self.lending.pk,))
            response = self.client.delete(url)
            # print(response.json())
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Lending.objects.all().count(), 1)

        def test_lending_issuance_delete(self):
            """Тест выдачи книги читателю."""
            url = reverse("library:lending_create")
            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "operation": "issuance",
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Lending.objects.all().count(), 2)

            url = reverse("library:lending_delete", args=(self.lending.pk,))
            response = self.client.delete(url)
            # print(response.json())
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Lending.objects.all().count(), 1)

        def test_lending_return_delete(self):
            """Тест отмены возврата книги."""
            url = reverse("library:lending_create")
            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "operation": "issuance",
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Lending.objects.all().count(), 2)

            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "operation": "return",
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Lending.objects.all().count(), 3)

            url = reverse("library:lending_delete", args=(self.lending.pk,))
            response = self.client.delete(url)
            # print(response.json())
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Lending.objects.all().count(), 2)

        def test_lending_loss_delete(self):
            """Тест отмены утери книги."""
            url = reverse("library:lending_create")
            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "operation": "issuance",
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Lending.objects.all().count(), 2)

            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "operation": "loss",
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Lending.objects.all().count(), 3)

            url = reverse("library:lending_delete", args=(self.lending.pk,))
            response = self.client.delete(url)
            # print(response.json())
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Lending.objects.all().count(), 2)

        def test_lending_loss_write_off(self):
            """Тест списания утерянной книги."""
            url = reverse("library:lending_create")
            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "operation": "issuance",
            }
            response = self.client.post(url, data)
            lending_pk = self.lending.pk  # запоминаем id выдачи книги
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Lending.objects.all().count(), 2)

            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "operation": "loss",
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Lending.objects.all().count(), 3)

            url = reverse(
                "library:lending_update", args=(lending_pk,)
            )  #  эндпоинт выданной книги для пометки о списании
            data = {"is_write_off": "true"}
            response = self.client.patch(url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(data.get("is_write_off"), "true")
