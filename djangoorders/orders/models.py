from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    customer = models.ForeignKey(
        'customers.Customer', related_name='orders', on_delete=models.PROTECT)
    date = models.DateField()
    code = models.CharField(max_length=20)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    taken_by = models.ForeignKey(
        User, related_name='orders_taken', on_delete=models.PROTECT)

    def __str__(self):
        return f'({self.pk}) {self.code}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(
        'items.Item', related_name='orders', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.pk
