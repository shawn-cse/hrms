from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HRMSAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hrms_auth"
    verbose_name = _("HRMS Auth")
