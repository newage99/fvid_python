from django.contrib import admin

from .models import AnalyzeRun


@admin.register(AnalyzeRun)
class AnalyzeRunAdmin(admin.ModelAdmin):
    pass
