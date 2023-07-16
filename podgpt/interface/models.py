from django.db import models

# Create your models here.


class Music(models.Model):
    name = models.SlugField()
    _file = models.FileField(verbose_name='file')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'C - Music'


class Series(models.Model):
    name = models.CharField(max_length=200)
    music = models.ForeignKey(
        Music, on_delete=models.SET_NULL, null=True, blank=True)

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

    class Meta:
        verbose_name = 'Episode'
        verbose_name_plural = 'C - Episodes'

    def __str__(self):
        return self.name


class SeriesGenerator(models.Model):
    title = models.CharField(max_length=200)
    guide_lines = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    running = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    series = models.ForeignKey(
        Series, on_delete=models.SET_NULL, null=True, blank=True)

    total_episodes = models.IntegerField(
        verbose_name='Total Episodes', default=0)
    episodes_generated = models.IntegerField(
        verbose_name='Generated Episodes', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Series Generator'
        verbose_name_plural = 'A - Series Generators'
