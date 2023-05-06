from django.contrib import admin
from django.db.models.functions import Length

from .models import FVID


@admin.register(FVID)
class FVIDAdmin(admin.ModelAdmin):

    list_display = ['value']
    search_fields = ['value']

    def delete_length_six_fvids(self, request, queryset):
        annotated_fvids = queryset.annotate(value_len=Length('value'))
        fvids = annotated_fvids.filter(value_len=11)
        fvids.delete()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            new_actions = {
                "Delete FVID's with length=6": FVIDAdmin.delete_length_six_fvids
            }
            for action in new_actions:
                actions[action] = (new_actions[action], action, action)
        return actions
