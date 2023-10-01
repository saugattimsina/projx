from django.apps import AppConfig


class BinarytreeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "binarytree"

    def ready(self):
        import binarytree.signals
