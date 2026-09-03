from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HRMSDoumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hrms_documents"
    verbose_name = _("Documents")
