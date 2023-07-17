from django.contrib import admin, messages
from django.http.request import HttpRequest
from django_object_actions import action, DjangoObjectActions

from threading import Thread

from .models import SeriesGenerator, Music, Series, Episode
from script.series_generator.generate import generate_series
from script.models import Script


@admin.register(SeriesGenerator)
class _SeriesGenerator(DjangoObjectActions, admin.ModelAdmin):
    readonly_fields = ['timestamp', 'running', 'used',
                       'total_episodes', 'episodes_generated', 'series']
    list_display = ['title', 'running', 'used', 'series', 'timestamp']

    change_actions = ('generate',)

    def thread_func(self, obj: SeriesGenerator):
        obj.running = True
        obj.save()

        scripts: list[Script] = generate_series(obj.title, obj.guide_lines)

        series = Series.objects.create(name=obj.title, music=obj.music)

        for script in scripts:
            episode = Episode.objects.create(
                name=script.title,
                series=series,
                script=script
            )

        obj.running = False
        obj.used = True
        obj.save()

    @action(label='Generate', description='Generate an entire series')
    def generate(self, request, obj: SeriesGenerator):
        if obj.used:
            # return messages.warning(request, 'The Series has already been generated.')
            pass

        if obj.running:
            # return messages.warning(request, 'This Series is already being generated.')
            pass

        thread = Thread(target=self.thread_func, args=[obj], daemon=True)
        thread.start()

        return messages.success(request, 'The Series is being generated.')


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
