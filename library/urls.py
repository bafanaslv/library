from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from library.apps import LibraryConfig
from library.views import (LendingListApiView, LendingCreateApiView, LendingRetrieveApiView, LendingUpdateApiView,
                           LendingDestroyApiView, BooksViewSet, AuthorsViewSet)
from rest_framework.routers import SimpleRouter

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

router_authors = SimpleRouter()
router_authors.register(prefix="authors", viewset=AuthorsViewSet, basename="authors")
router_books = SimpleRouter()
router_books.register(prefix="books", viewset=BooksViewSet, basename="books")


urlpatterns = [
    path("lending/", LendingListApiView.as_view(), name="lending_list"),
    path("lending/create/", LendingCreateApiView.as_view(), name="lending_create"),
    path("lending/<int:pk>/", LendingRetrieveApiView.as_view(), name="lending_retrieve"),
    path("lending/update/<int:pk>/", LendingUpdateApiView.as_view(), name="lending_update"),
    path("lending/delete/<int:pk>/", LendingDestroyApiView.as_view(), name="lending_delete"),
]
urlpatterns += router_books.urls
urlpatterns += router_authors.urls
