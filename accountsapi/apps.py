from django.apps import AppConfig


class AccountsapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accountsapi"

    def ready(self):
        import accountsapi.signals
