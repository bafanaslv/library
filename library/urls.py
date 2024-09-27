from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from library.apps import LibraryConfig
from library.views import (AuthorsListApiView, AuthorsCreateApiView, AuthorsRetrieveApiView, AuthorsUpdateApiView,
                           AuthorsDestroyApiView, BooksListApiView, BooksCreateApiView, BooksRetrieveApiView,
                           BooksUpdateApiView, BooksDestroyApiView, LendingListApiView, LendingCreateApiView,
                           LendingRetrieveApiView, LendingUpdateApiView, LendingDestroyApiView)

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API управления библиотекой.",
        terms_of_service="http://localhost:8000/library/",
        contact=openapi.Contact(email="foxship@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

app_name = LibraryConfig.name


urlpatterns = [
    path("authors/", AuthorsListApiView.as_view(), name="authors_list"),
    path("authors/create/", AuthorsCreateApiView.as_view(), name="author_create"),
    path("authors/<int:pk>/", AuthorsRetrieveApiView.as_view(), name="author_retrieve"),
    path("authors/update/<int:pk>/", AuthorsUpdateApiView.as_view(), name="author_update"),
    path("authors/delete/<int:pk>/", AuthorsDestroyApiView.as_view(), name="author_delete"),
    path("books/", BooksListApiView.as_view(), name="books_list"),
    path("books/create/", BooksCreateApiView.as_view(), name="book_create"),
    path("books/<int:pk>/", BooksRetrieveApiView.as_view(), name="book_retrieve"),
    path("books/update/<int:pk>/", BooksUpdateApiView.as_view(), name="book_update"),
    path("books/delete/<int:pk>/", BooksDestroyApiView.as_view(), name="book_delete"),
    path("lending/", LendingListApiView.as_view(), name="lending_list"),
    path("lending/create/", LendingCreateApiView.as_view(), name="lending_create"),
    path("lending/<int:pk>/", LendingRetrieveApiView.as_view(), name="lending_retrieve"),
    path("lending/update/<int:pk>/", LendingUpdateApiView.as_view(), name="lending_update"),
    path("lending/delete/<int:pk>/", LendingDestroyApiView.as_view(), name="lending_delete"),
]
