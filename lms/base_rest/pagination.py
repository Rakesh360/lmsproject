
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next_page': self.get_next_link(),
                'previous_page': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })