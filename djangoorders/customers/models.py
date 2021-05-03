from django.db import models


class Customer(models.Model):
    PH = 'ph'
    COUNTRY_CHOICES = (
        (PH, 'Philippines'),
    )

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    street = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    state = models.CharField(max_length=250, blank=True)
    zip_code = models.CharField(max_length=250, blank=True)
    country = models.CharField(
        max_length=250, blank=True, default=PH, choices=COUNTRY_CHOICES)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
