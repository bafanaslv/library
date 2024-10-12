from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Authors, Books, Lending
from users.models import Users
from users.permissions import IsLibrarian


class AuthorTestCase(APITestCase):
    """Тестирование CRUD курсов."""

    def setUp(self):
        self.user = Users.objects.create(
            email="ivc@foxship.ru",
            password="123qwe",
            is_superuser=True,
        )
        self.author = Authors.objects.create(
            author="Джек Лондон"
        )
        self.book = Books.objects.create(
            name="Любовь к жизни",
            genre="story",
            barcode="1111111111",
            author=self.author,
        )
        self.client.force_authenticate(user=self.user)

    def test_book_retrieve(self):
        url = reverse("library:books-detail", args=(self.book.pk,))
        response = self.client.get(url)
        # print(response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.book.name)

    def test_book_create(self):
        url = reverse("library:books-list")
        data = {
            "name": "Костер",
            "genre": "story",
            "barcode": "1111111111",
            "author": self.author,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Books.objects.all().count(), 2)

    # def test_course_update(self):
    #     url = reverse("courses:courses-detail", args=(self.course.pk,))
    #     data = {"name": "Физика", "description": "Любимый"}
    #     response = self.client.patch(url, data)
    #     #  print(response.json())
    #     data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("name"), "Физика")

#     def test_course_delete(self):
#         url = reverse("courses:courses-detail", args=(self.course.pk,))
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Courses.objects.all().count(), 0)
#
#     def test_course_list(self):
#         url = reverse("courses:courses-list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class LessonTestCase(APITestCase):
#     """Тестирование CRUD уроков."""
#
#     def setUp(self):
#         self.user = User.objects.create(email="foxship@yandex.ru")
#         self.course = Courses.objects.create(
#             name="Физика", description="Любимый курс", owner=self.user
#         )
#         self.lesson = Lessons.objects.create(
#             name="Механика",
#             course=self.course,
#             description="Интересный",
#             owner=self.user,
#         )
#         self.client.force_authenticate(user=self.user)
#
#     def test_lesson_retrieve(self):
#         url = reverse("courses:lessons_retrieve", args=(self.lesson.pk,))
#         response = self.client.get(url)
#         # print(response.json())
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get("name"), self.lesson.name)
#
#     def test_lesson_create(self):
#         url = reverse("courses:lessons_create")
#         data = {
#             "name": "Физика",
#             "course": self.course.pk,
#             "description": "Любимый курс",
#             "owner": self.user.pk,
#         }
#         response = self.client.post(url, data)
#         # print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Lessons.objects.all().count(), 2)
#
#     def test_lesson_update(self):
#         url = reverse("courses:lessons_update", args=(self.lesson.pk,))
#         data = {"name": "Физика", "course": self.course.pk}
#         response = self.client.patch(url, data)
#         data = response.json()
#         # print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get("name"), "Физика")
#
#     def test_lesson_delete(self):
#         url = reverse("courses:lessons_delete", args=(self.lesson.pk,))
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Lessons.objects.all().count(), 0)
#
#     def test_lesson_list(self):
#         url = reverse("courses:lessons_list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class SubscriptionTestCase(APITestCase):
#     """Тестирование актавации/деактивации подписки на курс."""
#
#     def setUp(self):
#         self.user = User.objects.create(email="foxship@yandex.ru")
#         self.course = Courses.objects.create(name="Физика")
#         self.subscription = Subscription.objects.create(
#             user=self.user, course=self.course
#         )
#         self.client.force_authenticate(user=self.user)
#
#     def test_subscription_create(self):
#         Subscription.objects.all().delete()
#         url = reverse("courses:courses_subscribe")
#         data = {"user": self.user.pk, "course": self.course.pk}
#         response = self.client.post(url, data)
#         # print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Subscription.objects.all()[0].course, self.course)
#
#     def test_subscription_delete(self):
#         url = reverse("courses:courses_subscribe")
#         response = self.client.post(url, {"course": self.course.pk})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Subscription.objects.count(), 0)
