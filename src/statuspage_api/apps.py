from django.apps import AppConfig


class StatuspageApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statuspage_api'

    def ready(self):
        from . import signals
