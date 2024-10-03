from django.contrib import admin
from django.urls import include, path
from library.urls import schema_view

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
