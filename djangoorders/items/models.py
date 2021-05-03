from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'({self.pk}) {self.name}'
