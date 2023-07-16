from django.contrib import admin

from .models import Script
# Register your models here.


@admin.register(Script)
class _Script(admin.ModelAdmin):
    pass
