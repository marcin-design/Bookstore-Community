from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Book, UserProfile, Friendship, Review, Wishlist
from .forms import *


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request,
                      'bookstore_app/registration.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return render(request,
                          'bookstore_app/main.html',
                          {'form': form})
        else:
            return render(request,
                          'bookstore_app/incorrect_registration.html',
                          {'form': form})

