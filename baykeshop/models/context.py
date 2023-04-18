from django.db.models.base import ModelBase
from django.db.models.fields.files import ImageField


class BaykeModelContext:
    """ 获取model的上下文 """
    def __init__(
        self, 
        modclass:ModelBase, 
        values_fields:list = None, 
        filter_fields:dict = None, 
        context_name:str = '_datas'
    ) -> None:
        
        self.modclass = modclass
        self.values_fields = values_fields
        self.filter_fields = filter_fields
        self.context_name = context_name
        self._context = {}
        
    def all_queryset(self):
        return self.modclass.objects.all()
    
    def filter_queryset(self):
        return self.all_queryset().filter(**(self.filter_fields or {}))
    
    def _values_queryset(self):
        if isinstance(self.values_fields, (list or tuple)) and len(self.values_fields) > 1:
            queryset = self.filter_queryset().values(*list(self.values_fields))
        elif isinstance(self.values_fields, str):
            queryset = self.filter_queryset().values_list(self.values_fields, flat=True)
        else:
            queryset = self.filter_queryset().values()
        
        for qs in queryset:
            keys = list(qs.keys())
            keys.remove('id')
            for field_name in keys:
                if isinstance(self.modclass._meta.get_field(field_name), ImageField):
                    qs[field_name] = f'/media/{qs[field_name]}' 
        return queryset
    
    def values_queryset(self):
        return list(self._values_queryset())
    
    def context(self, extra_context=None) -> dict:
        self._context[self.context_name] = self.values_queryset()
        self._context.update(**(extra_context or {}))
        return self._context
        
