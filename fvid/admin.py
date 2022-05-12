from django.contrib import admin

from .models import FVID


@admin.register(FVID)
class FVIDAdmin(admin.ModelAdmin):

    list_display = ['value']
    search_fields = ['value']
