from django.db import models

# Create your models here.


class Audio(models.Model):
    name = models.CharField(max_length=200)
    audio_file = models.FileField(verbose_name='file')
