from django.contrib import admin


from .models import SeriesGenerator, Music, Series
# Register your models here.


@admin.register(SeriesGenerator)
class _SeriesGenerator(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'running', 'used',
                       'total_episodes', 'episodes_generated', 'series']
    list_display = ['title', 'running', 'used', 'series', 'timestamp']


@admin.register(Series)
class _Series(admin.ModelAdmin):
    pass


@admin.register(Music)
class _Music(admin.ModelAdmin):
    pass
