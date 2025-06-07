from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # Number of messages per page
    page_size_query_param = 'page_size'  # Allow client to override, optional
    max_page_size = 100  # Maximum allowed page size to prevent abuse
