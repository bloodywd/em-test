from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator


class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('ready', 'Ready'),
        ('paid', 'Paid'),
    ]

    table_number = models.IntegerField(validators=[MinValueValidator(1)])

    total_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      default=0,
                                      validators=[MinValueValidator(0)])

    status = models.CharField(
        choices=STATUS_CHOICES,
        default='waiting',
        max_length=20
    )

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'order #{self.id}'

    def update_total_price(self):
        self.total_price = self.items.aggregate(total=Sum('price'))[
                               'total'] or 0
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items')
    dish_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.dish_name} - {self.price} Р'
