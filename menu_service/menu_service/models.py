from django.db import models


class Restaurants(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Menus(models.Model):
    date = models.DateField()
    items = models.JSONField()
    employers = models.JSONField(default=dict())
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
