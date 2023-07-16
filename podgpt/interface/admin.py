from django.contrib import admin
from django.http.request import HttpRequest
from django_object_actions import DjangoObjectActions, action

from threading import Thread

from .models import SeriesGenerator, Music, Series, Episode
# Register your models here.


@admin.register(SeriesGenerator)
class _SeriesGenerator(DjangoObjectActions, admin.ModelAdmin):
    readonly_fields = ['timestamp', 'running', 'used',
                       'total_episodes', 'episodes_generated', 'series']
    list_display = ['title', 'running', 'used', 'series', 'timestamp']

    change_actions = ('generate',)

    @action(label='Generate', description='Generate an entire series')
    def generate(self, request, obj: SeriesGenerator):
        pass


class _EpisodeInline(admin.StackedInline):
    model = Episode

    def has_add_permission(self, request: HttpRequest, obj) -> bool:
        return False  # super().has_add_permission(request)

    def has_change_permission(self, request: HttpRequest, obj) -> bool:
        return False  # super().has_change_permission(request, obj)


@admin.register(Episode)
class _Episode(admin.ModelAdmin):
    list_filter = ('series',)
    ordering = ('timestamp',)
    readonly_fields = ('timestamp',)
    list_display = ('name', 'series', 'timestamp',)


@admin.register(Series)
class _Series(admin.ModelAdmin):
    inlines = [_EpisodeInline]


@admin.register(Music)
class _Music(admin.ModelAdmin):
    pass
