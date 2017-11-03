from django.apps import AppConfig

class TestsConfig(AppConfig):
    name = 'abscrete.tests'

    def ready(self):
        from abscrete.models import abscrete_application_ready
        abscrete_application_ready(self)
