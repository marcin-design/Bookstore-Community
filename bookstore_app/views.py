from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Book, UserProfile, Friendship, Review, Wishlist
from .forms import *
import requests
from Bookstore_project import settings


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request,
                      'bookstore_app/registration.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('main.html')
        else:
            return render(request,
                          'bookstore_app/incorrect_registration.html',
                          {'form': form})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'bookstore_app/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = User.objects.filter(Q(username=username) | Q(email=email)).first()
            if user:
                return redirect('main')
            else:
                return render(request, 'bookstore_app/login.html', {'form': form})



def main_page(request):
    api_url = "https://www.googleapis.com/books/v1/volumes"
    api_key = settings.GOOGLE_BOOKS_API_KEY

    params = {
        "q": "Harry Potter",
        "key": api_key,
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        books = data.get("items", [])
    else:
        books = []

    return render(request,
                  'bookstore_app/main.html',
                  {'books': books})

