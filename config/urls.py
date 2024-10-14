from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from library.urls import schema_view
from library.views import AuthorsViewSet, BooksViewSet

router_authors = SimpleRouter()
router_authors.register("authors", AuthorsViewSet, basename="authors")
router_books = SimpleRouter()
router_books.register("books", BooksViewSet, basename="books")

urlpatterns = [
    path("", include("library.urls", namespace="library")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
urlpatterns += router_books.urls
urlpatterns += router_authors.urls
