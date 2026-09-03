from django.apps import AppConfig
from django.conf import settings


class HRMSMeetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hrms_meet"
    verbose_name = "Meet"

    def ready(self):
        from django.urls import include, path

        from hrms.urls import urlpatterns
        from hrms_meet import signals

        settings.APPS.append("hrms_meet")

        urlpatterns.append(
            path("meet/", include("hrms_meet.urls")),
        )
        super().ready()
