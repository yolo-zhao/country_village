from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.apps.activities'
    verbose_name = '乡村活动'

    def ready(self):
        import backend.apps.activities.signals

