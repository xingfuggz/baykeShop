from rest_framework.pagination import PageNumberPagination as DrfPageNumberPagination
from baykeshop.conf import bayke_settings


class PageNumberPagination(DrfPageNumberPagination):
    """ 商品分页 """
    page_size = bayke_settings.PAGE_SIZE
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = bayke_settings.MAX_PAGE_SIZE
    
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data.update({
                'page_size': self.page_size,
                'pages': [ i for i in self.page.paginator.get_elided_page_range()],
                'current': int(self.request.query_params.get('page', 1))
            })
        return response
   