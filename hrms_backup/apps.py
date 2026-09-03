from django.apps import AppConfig


class BackupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hrms_backup"

    def ready(self):
        from django.urls import include, path

        from hrms.urls import urlpatterns

        urlpatterns.append(
            path("backup/", include("hrms_backup.urls")),
        )
        super().ready()
