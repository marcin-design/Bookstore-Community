from datetime import datetime

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Book, UserProfile, Friendship, Review, Wishlist, User
from .forms import RegistrationForm, LoginForm, FriendsListForm, WishlistForm, AddFriendForm
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
            return redirect('main')
        else:
            return render(request,
                          'bookstore_app/incorrect_registration.html',
                          {'form': form})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request,
                      'bookstore_app/login.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                return render(request, 'bookstore_app/login.html', {'form': form})
        else:
            return render(request, 'bookstore_app/login.html', {'form': form})


@login_required
def main_page(request, book_id=None):
    if book_id:
        try:
            # Konwertuj identyfikator książki z ciągu znaków na liczbę całkowitą
            book_id_int = int(book_id)

            # Znajdź książkę w bazie danych używając nowego identyfikatora
            book = Book.objects.get(pk=book_id_int)

            return render(request, 'bookstore_app/book_details.html', {'book': book})
        except (ValueError, Book.DoesNotExist):
            raise Http404("Book does not exist")
    else:
        #the function aims to retrieve data from the Google Books API,
        # process it and save it in the database based on the Book model
        api_url = "https://www.googleapis.com/books/v1/volumes"
        api_key = settings.GOOGLE_BOOKS_API_KEY

        params = {
            "q": "Grace",
            "key": api_key,
        }

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            books = data.get("items", [])

            for book_data in books:
                book_info = book_data.get("volumeInfo", {})
                genres = book_info.get("categories", [])

                existing_book = Book.objects.filter(title=book_info.get("title", ""))

                if not existing_book:
                    thumbnail = book_info.get("imageLinks", {}).get("thumbnail", "")

                    def convert_to_date(date_str):
                    #function that tries to convert a date from a custom format to a date object(Y-M-D)
                        try:
                            date = datetime.strptime(date_str, "%Y").date()
                            return date
                        except ValueError:
                            return None

                    new_book = Book(
                        title=book_info.get("title", ""),
                        author=",".join(book_info.get("authors", [])),
                        description=book_info.get("description", ""),
                        published_date=convert_to_date(book_info.get("publishedDate")),
                        genre=",".join(genres),
                        user_rating=None,
                        thumbnail=thumbnail
                    )

                    new_book.save()

        else:
            books = []

        return render(request,
                      'bookstore_app/main.html',
                      {'books': books})


class BookDetailsView(View):
    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        return render(request,
                      'bookstore_app/book_details.html',
                      {'book': book})

def logout_view(request):
    logout(request)
    return render(request, 'bookstore_app/logout.html')

class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'bookstore_app/user_profile.html')


    def post(self, request, *args, **kwargs):
        return redirect('user_profile')

class AddFriendView(View):
    def get(self, request):
        form = AddFriendForm()
        return render(request, 'bookstore_app/add_friend.html', {'form': form})

    def post(self, request):
        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend_username = form.cleaned_data['friend_username']
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            try:
                friend = User.objects.get(username=friend_username)

                if friend != request.user:
                    friend_profile, _ = UserProfile.objects.get_or_create(user=friend)
                    user_profile.friends.add(friend_profile)

            except UserProfile.DoesNotExist:
                return redirect('bookstore_app/user_does_not_exists.html')

        return HttpResponseRedirect(request.path_info)


class FriendsListView(View):
    def get(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        friends = user_profile.friends.all()
        return render(request,
                      'bookstore_app/friends_list.html',
                      {'friends': friends})




class WishlistView(View):
    def get(self, request, *args, **kwargs):
        form = WishlistForm()
        return render(request,
                      'bookstore_app/wishlist.html',
                      {'form': form})


class BooksReadView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'bookstore_app/books_read.html')
