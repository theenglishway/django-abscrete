from django.apps import AppConfig


class ExampleAppConfig(AppConfig):
    name = 'example_app'

    def ready(self):
        from abscrete.models import abscrete_application_ready
        abscrete_application_ready(self)