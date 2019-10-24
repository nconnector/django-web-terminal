from django.apps import AppConfig


class DashKijijiConfig(AppConfig):
    name = 'dash_kijiji'

    def ready(self):
        from . import signals