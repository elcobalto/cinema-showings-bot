from django.db import models

from apps import Cinema


class Showing(models.Model):
    movie_title = models.CharField(max_length=255)
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE,
        related_name="showings",
    )
    date = models.CharField(max_length=255)
    datetime = models.CharField(max_length=255)
    format = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=255)
