from django.db import models

from script.models import Script
from audio.models import Audio


class Music(models.Model):
    name = models.SlugField()
    _file = models.FileField(verbose_name='file')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'D - Music'


class Series(models.Model):
    name = models.CharField(max_length=200)

    def episodes(self):
        return Episode.objects.filter(series=self).all()

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = 'B - Series'

    def __str__(self):
        return self.name


class Episode(models.Model):
    name = models.CharField(max_length=200)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    script = models.ForeignKey(
        Script, on_delete=models.CASCADE, null=True, blank=True)
    episode_number = models.IntegerField(default=0)
    audio = models.ForeignKey(
        Audio, on_delete=models.SET_NULL, default=None, null=True)

    class Meta:
        verbose_name = 'Episode'
        verbose_name_plural = 'D - Episodes'

    def __str__(self):
        return self.name


class SeriesGenerator(models.Model):
    title = models.CharField(max_length=200)
    guide_lines = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    running = models.BooleanField(
        default=False, verbose_name='Script generator running')
    used = models.BooleanField(default=False, verbose_name='Script generated')
    series = models.ForeignKey(
        Series, on_delete=models.SET_NULL, null=True, blank=True)
    audio_generator_running = models.BooleanField(default=False)
    audio_generated = models.BooleanField(default=False)
    remixing = models.BooleanField(default=False)
    remixed = models.BooleanField(default=False)

    music = models.ForeignKey(
        Music,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_music',
        blank=True
    )

    intro = models.ForeignKey(
        Music,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_intro',
        blank=True
    )

    outro = models.ForeignKey(
        Music,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_outro',
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Generator'
        verbose_name_plural = 'A - Generators'


class Plug(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Plug'
        verbose_name_plural = 'C - Plug'
