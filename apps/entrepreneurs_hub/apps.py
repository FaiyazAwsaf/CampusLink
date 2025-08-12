from django.apps import AppConfig


class EntrepreneursHubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.entrepreneurs_hub'
    
    def ready(self):
        import apps.entrepreneurs_hub.signals
