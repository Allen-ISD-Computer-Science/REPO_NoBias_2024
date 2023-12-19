from django.db import models

# Create your models here.
class Link(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link