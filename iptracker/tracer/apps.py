from django.apps import AppConfig


class TracerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracer'

    def ready(self):
        from tracer import updater
        updater.start()
