from baykeshop.public.pagination import PageNumberPagination


class OrderInfoPageNumberPagination(PageNumberPagination):
    """ 订单分页 """
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100