from django.contrib import admin

from .models import AnalyzeRun


@admin.register(AnalyzeRun)
class AnalyzeRunAdmin(admin.ModelAdmin):

    list_display = ['id', 'fvid_length', 'number_of_nodes', 'upload_frequency', 'next_fvid_to_analyze', '_percentage',
                    '_completed']

    def _percentage(self, obj):
        return f"{obj.percentage}%"

    def _completed(self, obj):
        return bool(obj and obj.completed_at)
    _completed.boolean = True
