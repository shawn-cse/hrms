"""
admin.py
"""

from django.contrib import admin

from hrms_audit.models import AuditTag, HRMSAuditInfo, HRMSAuditLog

# Register your models here.

admin.site.register(AuditTag)
