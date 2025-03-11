from django.test import TestCase
from django.urls import reverse
from em_project.orders.models import Order, OrderItem


class OrderViewTests(TestCase):

    def setUp(self):
        self.order = Order.objects.create(
            table_number=1,
        )

        self.item1 = OrderItem.objects.create(order=self.order,
                                              dish_name='Dish 1', price=50.0)
        self.item2 = OrderItem.objects.create(order=self.order,
                                              dish_name='Dish 2', price=50.0)
        self.order.update_total_price()

        self.create_url = reverse('create_order')
        self.order_detail_url = reverse('view_order', args=[self.order.pk])
        self.edit_order_url = reverse('edit_order_items', args=[self.order.pk])
        self.delete_order_url = reverse('delete_order_by_id',
                                        args=[self.order.pk])
        self.update_order_url = reverse('edit_status', args=[self.order.pk])
        self.income = reverse('income')

    def test_order_create_view(self):
        response = self.client.post(self.create_url, {
            'table_number': 2,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 2)

    def test_order_detail_view(self):
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dish 1')

    def test_order_update_view(self):
        self.client.post(self.update_order_url, {
            'status': 'ready',
        })
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'ready')

    def test_order_delete_view(self):
        response = self.client.post(self.delete_order_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_items_edit_view(self):
        response = self.client.get(self.edit_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dish 1')

    def test_order_item_addition(self):
        response = self.client.post(self.edit_order_url, {
            'dish_name': 'Dish 3',
            'price': 80.0
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderItem.objects.count(), 3)

    def test_order_item_deletion(self):
        item_count_before = OrderItem.objects.count()
        response = self.client.post(self.edit_order_url, {
            'delete_item': self.item1.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderItem.objects.count(), item_count_before - 1)

    def test_create_order_invalid_data(self):
        response = self.client.post(self.create_url, {
            'table_number': -1,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Ensure this value is greater than or equal to 1.')

    def test_calculate_income_view(self):
        paid_order = Order.objects.create(
            table_number=3,
            status='paid'
        )
        OrderItem.objects.create(order=paid_order, dish_name='Dish 1',
                                 price=150.0)
        OrderItem.objects.create(order=paid_order, dish_name='Dish 2',
                                 price=150.0)

        response = self.client.get(self.income)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total Income: 300.00 Р')


class OrderItemModelTest(TestCase):

    def test_order_item_creation(self):
        order = Order.objects.create(table_number=1)
        item = OrderItem.objects.create(order=order, dish_name='Dish 1',
                                        price=50.0)
        order.update_total_price()

        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(item.dish_name, 'Dish 1')
        self.assertEqual(item.price, 50.0)
        self.assertEqual(item.order, order)
