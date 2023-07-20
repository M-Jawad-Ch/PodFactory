from django.db import models

# Create your models here.


class Script(models.Model):
    title = models.CharField(max_length=200)
    contents = models.TextField()

    class Meta:
        verbose_name = 'Script'

    def __str__(self):
        return self.title
