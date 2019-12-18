"""Register all incident app models here."""
from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class SectorAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(AffectedUnit)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Incident)
admin.site.register(Related_ip)
admin.site.register(Related_domain)
admin.site.register(Task)
# admin.site.register(Comment)
