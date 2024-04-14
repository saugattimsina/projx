from django.apps import AppConfig


class SignalbotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "signalbot"

    def ready(self):
        import signalbot.signals

        # import signalbot.recivers
