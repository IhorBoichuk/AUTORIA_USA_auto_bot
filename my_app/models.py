from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    auto_ria_link = models.URLField(unique=True)
    auction_link = models.URLField()
    photo_urls = models.JSONField()

