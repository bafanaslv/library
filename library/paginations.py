from rest_framework.pagination import PageNumberPagination


class AuthorsPaginator(PageNumberPagination):
    page_size = 5
    page_query_param = "page_size"
    max_page_size = 10


class BooksPaginator(PageNumberPagination):
    page_size = 5
    page_query_param = "page_size"
    max_page_size = 10


class LendingPaginator(PageNumberPagination):
    page_size = 5
    page_query_param = "page_size"
    max_page_size = 10
