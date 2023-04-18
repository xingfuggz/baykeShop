from django.conf import settings

from baykeshop.conf.defaults import bayke_defaults


class Settings:
    
    def __init__(self, config_name:str=None) -> None:
        self.config_name = config_name or "BAYKE_SHOP"
        
    def __getattr__(self, attr):
        defaults = getattr(settings, self.config_name, {**bayke_defaults})
        try:
            val = defaults[attr]
        except KeyError:
            raise AttributeError("Invalid API setting: '%s'" % attr)
        return val
            
        
bayke_settings = Settings()