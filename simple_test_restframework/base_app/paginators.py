from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20

    def get_paginated_response(self, data):
        # Customize the response format if needed
        return Response({
            'total_records': self.count,
            'next_page': self.get_next_link(),
            'prev_page': self.get_previous_link(),
            'data': data,
        })
