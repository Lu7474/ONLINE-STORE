from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cart, Product
from django.test import TestCase, Client
from django.urls import reverse


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(name="Test Product", price=100.0)
        self.cart = Cart.objects.create(
            user=self.user, product=self.product, quantity=2
        )

    def test_products_price(self):
        self.assertEqual(self.cart.products_price(), 200.0)

    def test_cart_str_with_user(self):
        expected_str = f"Корзина {self.user.username} | Товар {self.product.name} | Количество {self.cart.quantity}"
        self.assertEqual(str(self.cart), expected_str)

    def test_cart_str_anonymous(self):
        anonymous_cart = Cart.objects.create(product=self.product, quantity=1)
        expected_str = f"Анонимная корзина | Товар {self.product.name} | Количество {anonymous_cart.quantity}"
        self.assertEqual(str(anonymous_cart), expected_str)


class CartChangeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cart = Cart.objects.create(quantity=1)
        self.url = reverse("cart_change")

    def test_cart_change_quantity(self):
        response = self.client.post(self.url, {"cart_id": self.cart.id, "quantity": 2})
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.quantity, 2)
        self.assertEqual(response.status_code, 302)

    def test_cart_delete(self):
        response = self.client.post(self.url, {"cart_id": self.cart.id, "quantity": 0})
        with self.assertRaises(Cart.DoesNotExist):
            self.cart.refresh_from_db()
        self.assertEqual(response.status_code, 302)


class CartRemoveViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cart = Cart.objects.create(quantity=1)
        self.url = reverse("cart_remove")

    def test_cart_remove(self):
        response = self.client.post(self.url, {"cart_id": self.cart.id})
        with self.assertRaises(Cart.DoesNotExist):
            self.cart.refresh_from_db()
        self.assertEqual(response.status_code, 302)
