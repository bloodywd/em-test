from django.db import models
from django.db.models import Sum


class Dish(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __self__(self):
        return f'{self.name} - {self.price}Р'



class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()

    total_price = models.DecimalField(max_digits=9, decimal_places=2)

    status = models.CharField(
        choices=STATUS_CHOICES,
        default='waiting',
        max_length=20
    )

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __self__(self):
        return f'Заказ {self.id}'


    def update_total_price(self):
        self.total_price = self.items.aggregate(total=Sum('dish__price'))['total'] or 0
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
