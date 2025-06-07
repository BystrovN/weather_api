from django.db import models


class ForecastOverride(models.Model):
    city = models.CharField(max_length=255)
    date = models.DateField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()

    def __str__(self) -> str:
        return f'{self.city} -> {self.date}'
