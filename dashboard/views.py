from django.db import DatabaseError
from django.db.models import Sum
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from .models import


def index(request):
    context = {
        # "categories": categories,
    }
    return render(request, "index.html", context)
