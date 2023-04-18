from baykeshop.public.pagination import PageNumberPagination


class PageNumberPagination(PageNumberPagination):
    """ 商品分页 """
    page_size = 10
    max_page_size = 10000