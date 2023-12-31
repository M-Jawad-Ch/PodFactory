from django.contrib import admin, messages
from django.http.request import HttpRequest
from django_object_actions import action, DjangoObjectActions
from django.contrib.sites.models import Site

import json

from threading import Thread
from pydub import AudioSegment

from .models import SeriesGenerator, Music, Series, Episode, Plug
from script.series_generator.generate import generate_series
from script.models import Script
from audio.generator.elevenlabs import AudioSynthesiser
from audio.generator.designer import add_music, intro_outro


@admin.register(SeriesGenerator)
class _SeriesGenerator(DjangoObjectActions, admin.ModelAdmin):
    readonly_fields = [
        'timestamp',
        'running',
        'used',
        'series',
        'audio_generator_running',
        'audio_generated',
        'remixing',
        'remixed'
    ]

    list_display = ['title', 'running', 'used', 'series', 'timestamp']

    change_actions = ('generate', 'synthesize', 'remix')

    def series_thread_func(self, obj: SeriesGenerator):
        obj.running = True
        obj.save()

        plug = Plug.objects.first()

        try:
            scripts: list[Script] = generate_series(
                obj.title, obj.guide_lines, plug.content if plug else '')
        except Exception as e:
            print(e)
            obj.running = False
            obj.used = False
            obj.save()
            return

        series = Series.objects.create(name=obj.title)

        episodes: list[Episode] = []

        for idx, script in enumerate(scripts):
            episodes.append(Episode.objects.create(
                name=script.title,
                series=series,
                script=script,
                episode_number=idx + 1
            ))

        obj.series = series

        obj.running = False
        obj.used = True
        obj.save()

    @action(label='Generate', description='Generate an entire series')
    def generate(self, request, obj: SeriesGenerator):
        if obj.used:
            return messages.warning(request, 'The Series has already been generated.')

        if obj.running:
            return messages.warning(request, 'This Series is already being generated.')

        Thread(
            target=self.series_thread_func,
            args=[obj],
            daemon=True
        ).start()

        return messages.success(request, 'The Series is being generated.')

    def audio_thread_func(self, obj: SeriesGenerator):
        obj.audio_generator_running = True
        obj.audio_generated = False
        obj.save()

        synthesiser = AudioSynthesiser()
        episodes = obj.series.episodes()

        for episode in episodes:
            if episode.audio:
                episode.audio.delete()
                episode.audio.save()

            episode.audio = synthesiser.generate(
                episode.name,
                json.loads(episode.script.contents)
            )

            episode.save()

        obj.audio_generator_running = False
        obj.audio_generated = True
        obj.save()

    @action(label='Synthesize', description='Generate Audio')
    def synthesize(self, request, obj: SeriesGenerator):
        if obj.audio_generated:
            return messages.warning(request, 'The audio has already been generated.')

        if obj.audio_generator_running:
            return messages.warning(request, 'The audio is already being generated.')

        Thread(
            target=self.audio_thread_func,
            args=[obj],
            daemon=True
        ).start()

        return messages.success(request, 'The audio generation has started.')

    def remix_thread_function(self, generator: SeriesGenerator):
        generator.remixing = True
        generator.remixed = False
        generator.save()

        episodes = generator.series.episodes()
        for episode in episodes:
            audio = episode.audio

            site = Site.objects.first()

            audio = add_music(audio, generator.music, site)
            audio = intro_outro(
                audio,
                generator.intro,
                generator.outro,
                site
            )

        generator.remixing = False
        generator.remixed = True
        generator.save()

    @action(label='Remix', description='Add Music')
    def remix(self, request, obj: SeriesGenerator):
        if obj.remixing:
            return messages.warn(request, 'The audio is already remixing.')

        if obj.remixed:
            return messages.warn(request, 'The audio has already remixed.')

        Thread(
            target=self.remix_thread_function,
            daemon=True,
            args=[obj]
        ).start()

        return messages.success(request, 'The remixing has started.')


class _EpisodeInline(admin.StackedInline):
    model = Episode

    def has_add_permission(self, request: HttpRequest, obj) -> bool:
        return False  # super().has_add_permission(request)

    def has_change_permission(self, request: HttpRequest, obj) -> bool:
        return False  # super().has_change_permission(request, obj)


@admin.register(Episode)
class _Episode(admin.ModelAdmin):
    list_filter = ('series',)
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    list_display = ('name', 'series', 'timestamp',)


@admin.register(Series)
class _Series(admin.ModelAdmin):
    inlines = [_EpisodeInline]


@admin.register(Music)
class _Music(admin.ModelAdmin):
    pass


@admin.register(Plug)
class _Plug(admin.ModelAdmin):
    pass
