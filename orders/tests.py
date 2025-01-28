from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Order, OrderItem
from dashboard.models import Products
from carts.models import Cart
from .forms import CreateOrderForm


class CreateOrderFormTest(TestCase):
    def test_create_order_form_valid_data(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "requires_delivery": "1",
            "delivery_address": "123 Test St",
            "payment_on_get": "1",
        }
        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_order_form_invalid_data(self):
        form_data = {
            "first_name": "",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "requires_delivery": "1",
            "delivery_address": "123 Test St",
            "payment_on_get": "1",
        }
        form = CreateOrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_create_order_form_optional_delivery_address(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "requires_delivery": "0",
            "delivery_address": "",
            "payment_on_get": "1",
        }
        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())


class OrderItemQuerysetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Products.objects.create(name="Test Product", price=100.0)
        self.order = Order.objects.create(user=self.user)
        self.order_item1 = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=2
        )
        self.order_item2 = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=3
        )

    def test_total_price(self):
        total_price = OrderItem.objects.all().total_price()
        self.assertEqual(total_price, 500.0)

    def test_total_quantity(self):
        total_quantity = OrderItem.objects.all().total_quantity()
        self.assertEqual(total_quantity, 5)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(user=self.user)

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, "testuser")


class CreateOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        self.url = reverse("create_order")

    def test_create_order_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_order_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "create_order.html")

    def test_create_order_view_initial_data(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertEqual(form.initial["first_name"], self.user.first_name)
        self.assertEqual(form.initial["last_name"], self.user.last_name)

    def test_create_order_view_form_valid(self):
        Cart.objects.create(
            user=self.user, product_id=1, quantity=1
        )  # Замените product_id на существующий ID продукта
        form_data = {
            "first_name": "Test",
            "last_name": "User",
            "address": "123 Test St",
            "city": "Test City",
            "postal_code": "12345",
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())
