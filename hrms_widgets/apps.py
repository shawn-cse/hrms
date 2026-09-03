from django.apps import AppConfig


class HRMSWidgetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hrms_widgets"

    def ready(self):
        from hrms_widgets.widgets.file_widgets import patch_clearable_file_input

        patch_clearable_file_input()
