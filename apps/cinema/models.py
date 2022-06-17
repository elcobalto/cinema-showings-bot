from django.db import models


class Town(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)


class Cinema(models.Model):
    CINEHOYTS = "CineHoyts"
    CINEMARK = "Cinemark"
    CINEPLANET = "Cineplanet"
    INDEPENDENT = "Independent"
    MUVIX = "Muvix"
    CHAIN_CHOICES = (
        (CINEHOYTS, CINEHOYTS),
        (CINEMARK, CINEMARK),
        (CINEPLANET, CINEPLANET),
        (INDEPENDENT, INDEPENDENT),
        (MUVIX, MUVIX),
    )
    name = models.CharField(max_length=255, unique=True)
    chain = models.CharField(max_length=255, choices=CHAIN_CHOICES)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, unique=True)
    town = models.ForeignKey(
        Town,
        on_delete=models.CASCADE,
        related_name="cinemas",
    )
