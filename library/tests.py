# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from courses.models import Courses, Lessons, Subscription
# from users.models import User
#
#
# class CourseTestCase(APITestCase):
#     """Тестирование CRUD курсов."""
#
#     def setUp(self):
#         self.user = User.objects.create(email="foxship@yandex.ru")
#         self.course = Courses.objects.create(
#             name="Физика", description="Любимый предмет", owner=self.user
#         )
#         self.lesson = Lessons.objects.create(
#             name="Оптика",
#             description="Один из лучших",
#             course=self.course,
#             owner=self.user,
#         )
#         self.client.force_authenticate(user=self.user)
#
#     def test_course_retrieve(self):
#         url = reverse("courses:courses-detail", args=(self.course.pk,))
#         response = self.client.get(url)
#         # print(response.json())
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get("name"), self.course.name)
#
#     def test_course_create(self):
#         url = reverse("courses:courses-list")
#         data = {"name": "Физика", "description": "Любимый"}
#         response = self.client.post(url, data)
#         #  print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Courses.objects.all().count(), 2)
#
#     def test_course_update(self):
#         url = reverse("courses:courses-detail", args=(self.course.pk,))
#         data = {"name": "Физика", "description": "Любимый"}
#         response = self.client.patch(url, data)
#         #  print(response.json())
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get("name"), "Физика")
#
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
