from django.contrib import admin

from .models import Audio

# Register your models here.


@admin.register(Audio)
class _Audio(admin.ModelAdmin):
    pass
