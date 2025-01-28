from django.test import TestCase
from django import forms
from .forms import UserRegistrationForm
from .models import User
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class UserRegistrationFormTest(TestCase):
    def test_user_registration_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "password123",
            "password2": "password123",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid_data(self):
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "password123",
            "password2": "differentpassword",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="12345"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser@example.com")

    def test_user_save_without_username(self):
        user = User.objects.create_user(
            email="nousername@example.com", password="12345"
        )
        user.username = ""
        user.save()
        self.assertEqual(user.username, "nousername@example.com")


class UserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        self.url = reverse("registration/profile")

    def test_user_profile_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "registration/profile.html")

    def test_user_profile_view_context(self):
        response = self.client.get(self.url)
        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"].username, "testuser")
