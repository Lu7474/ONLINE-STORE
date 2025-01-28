from django.test import TestCase, Client
from .models import Catalog
from django.urls import reverse


class CatalogModelTest(TestCase):
    def setUp(self):
        self.catalog = Catalog.objects.create(name="Test Catalog")

    def test_catalog_creation(self):
        self.assertEqual(self.catalog.name, "Test Catalog")

    def test_catalog_str(self):
        self.assertEqual(str(self.catalog), "Test Catalog")


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.catalog = Catalog.objects.create(name="Test Catalog")
        self.url = reverse("")

    def test_dashboard_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "index.html")

    def test_dashboard_view_context(self):
        response = self.client.get(self.url)
        self.assertIn("catalog", response.context)
        self.assertEqual(response.context["catalog"].name, "Test Catalog")
