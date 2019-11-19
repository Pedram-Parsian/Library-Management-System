from django.apps import AppConfig


class CirculationConfig(AppConfig):
    name = 'circulation'

    def ready(self):
        import circulation.signals
