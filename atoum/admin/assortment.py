from django.contrib import admin

from ..models import Assortment


@admin.register(Assortment)
class AssortmentAdmin(admin.ModelAdmin):
    pass
