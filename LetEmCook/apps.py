from django.apps import AppConfig


class LetemcookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LetEmCook'

    def ready(self):
        import LetEmCook.signals

