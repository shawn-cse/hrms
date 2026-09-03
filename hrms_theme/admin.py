"""
Admin registration for the hrms_theme app
"""

from django.contrib import admin

from hrms_theme.models import CompanyTheme, HRMSColorTheme

# Register your hrms_theme models here.
admin.site.register(HRMSColorTheme)
admin.site.register(CompanyTheme)
