from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from library.apps import LibraryConfig
from rest_framework.routers import SimpleRouter
from library.views import AuthorsViewSet, BooksListApiView

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
router = SimpleRouter()
router.register("", AuthorsViewSet, basename="authors")

urlpatterns = [
    path("", BooksListApiView.as_view(), name="books_list"),
]
urlpatterns += router.urls