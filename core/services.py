from django.utils.safestring import mark_safe
from django.urls import reverse


def create_admin_change_link(admin_reverse_url, obj_id, text):
    return mark_safe('<a href="{}">{}</a>'.format(reverse(f"admin:{admin_reverse_url}", args=(obj_id,)), text))
