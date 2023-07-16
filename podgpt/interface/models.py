from django.db import models

# Create your models here.


class Series(models.Model):

    def episodes(self):
        return Episode.objects.filter(series=self).all()

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = '(2) Series'


class Episode(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)


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
        verbose_name_plural = '(1) Series Generator'


class Music(models.Model):
    name = models.SlugField()
    _file = models.FileField(verbose_name='file')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = '(3) Music File'
