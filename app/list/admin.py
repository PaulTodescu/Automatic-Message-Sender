from django.contrib import admin

# Register your models here.

from .models import List


class ListsAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
    list_display_links = ['name', 'date']
    search_fields = ['name']


admin.site.register(List, ListsAdmin)
