from datetime import datetime

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Book, UserProfile, Friendship, Review, Wishlist, User, Notification
from .forms import RegistrationForm, LoginForm, FriendsListForm, WishlistForm, AddFriendForm, UserBooksForm, \
    CurrentlyReadingForm, UserRatingForm, RemoveFromWishlistForm, ReviewForm, RemoveFriendForm
import requests
from Bookstore_project import settings
from django.utils.dateparse import parse_date
from django.views.generic.detail import DetailView


class RegistrationView(View):
    #view which lets a user registration
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
    #view for logging in into store
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request,
                      'bookstore_app/login.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            #those two variables download data from form and are validated
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #this 'user' variable authenticates the user
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
            book_id_int = int(book_id)
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
            "q": "Heroes",
            "key": api_key,
        }

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            books = []
            # Processes the HTTP response and parses it as JSON
            data = response.json()
            google_books = data.get("items", [])

            for book_data in google_books:
                # Download information about a specific book
                book_info = book_data.get("volumeInfo", {})
                # Download book genres from book information
                genres = book_info.get("categories", [])
                # Check whether a book with a given title already exists in the database
                existing_book = Book.objects.filter(title=book_info.get("title", ""))

                for book in existing_book:
                    books.append(book)


                if not existing_book:
                    thumbnail = book_info.get("imageLinks", {}).get("thumbnail", "")


                    def convert_to_date(date_str):
                        # function that tries to convert a date from a custom format to a date object(Y-M-D)
                        if date_str:
                            try:
                                # parse_date used due to more flexibility about received format
                                date = parse_date(date_str)
                                return date
                            except ValueError:
                                return None
                        else:
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
                    books.append(new_book)
        else:
            books = []
        return render(request,
                      'bookstore_app/main.html',
                      {'books': books})


class BookDetailsView(View):
    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        reviews = Review.objects.filter(book=book)
        form = UserRatingForm()
        review_form = ReviewForm()
        return render(request, 'bookstore_app/book_details.html',
                      {'book': book,
                       'form': form,
                       'review_form': review_form,
                       'reviews': reviews})

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        form = UserRatingForm(request.POST)
        review_form = ReviewForm(request.POST)

        if form.is_valid():
            action = request.POST.get('action')
            if action == 'Like':
                if request.user not in book.liked_users.all():
                    if request.user not in book.disliked_users.all():
                        users_who_liked = book.liked_users.all()
                        for user in users_who_liked:
                            if user != request.user:
                                notification = Notification(
                                    recipient=user,
                                    sender=request.user,
                                    book=book,
                                    message=f"The user {request.user.username} gave a like to book: {book.title}"
                                )
                                notification.save()
                        book.likes += 1
                        book.liked_users.add(request.user)
                        book.save()

            elif action == "Dislike":
                if request.user not in book.disliked_users.all():
                    if request.user not in book.liked_users.all():
                        users_who_disliked = book.disliked_users.all()
                        for user in users_who_disliked:
                            if user != request.user:
                                notification = Notification(
                                    recipient=user,
                                    sender=request.user,
                                    book=book,
                                    message=f"The user {request.user.username} gave a dislike to book: {book.title}"
                                )
                                notification.save()
                        book.dislikes += 1
                        book.disliked_users.add(request.user)
                        book.save()

            elif action == "Add to Wishlist":
                wishlist, created = Wishlist.objects.get_or_create(user=request.user)
                if book not in wishlist.books.all():
                    wishlist.books.add(book)

                    users_who_added_to_wishlist = book.wishlisted_users.all()
                    for user in users_who_added_to_wishlist:
                        if user != request.user:
                            notification = Notification(
                                recipient=user,
                                sender=request.user,
                                message=f"The user {request.user.username} added a book: {book.title} to wishlist",
                            )
                            notification.save()

        if review_form.is_valid():
            #feature which letting a user to add comment in the specific book view
            action = request.POST.get('action')
            if action == 'Add review':
                review = review_form.save(commit=False)
                review.user = request.user
                review.book = book
                review.save()
                return redirect('book_details', book_id=book.id)

            reviews = Review.objects.filter(book=book)
            return render(request,
                          'bookstore_app/book_details.html',
                          {'book': book,
                           'form': form,
                           'review_form': review_form,
                           'reviews': reviews})
        else:
            return HttpResponse("Invalid action or form data.")


class InvalidFormView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "bookstore_app/invalid_form.html")

def logout_view(request):
    logout(request)
    return render(request, 'bookstore_app/logout.html')


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        #Handle notifications
        user_notifications = Notification.objects.filter(recipient=request.user)
        # Handle Wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        books_in_wishlist = wishlist.books.all()
        wishlist_form = WishlistForm()
        remove_from_wishlist_form = RemoveFromWishlistForm()

        # Handle UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        currently_reading_form = CurrentlyReadingForm(instance=user_profile)

        if user_profile.currently_reading_book:
            currently_reading_book_id = user_profile.currently_reading_book.id
        else:
            currently_reading_book_id = None
        request.session['currently_reading_book_id'] = currently_reading_book_id
        return render(request, 'bookstore_app/user_profile.html', {
            'wishlist_form': wishlist_form,
            'books_in_wishlist': books_in_wishlist,
            'currently_reading_form': currently_reading_form,
            'user_profile': user_profile,
            'notifications': user_notifications,
            'remove_from_wishlist_form': remove_from_wishlist_form,
        })

    def post(self, request, *args, **kwargs):
        # Handle Wishlist
        wishlist_form = WishlistForm(request.POST)
        remove_from_wishlist_form = RemoveFromWishlistForm(request.POST)
        if wishlist_form.is_valid():
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            books_to_add = wishlist_form.cleaned_data.get('books')
            wishlist.books.add(*books_to_add)

        # Handle UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            currently_reading_form = CurrentlyReadingForm(request.POST, instance=user_profile)
            if currently_reading_form.is_valid():
                currently_reading_form.save()

                if user_profile.currently_reading_book:
                    request.session['currently_reading_book_id'] = user_profile.currently_reading_book.id
                else:
                    request.session['currently_reading_book_id'] = None

        if request.method == 'POST':
            if 'action' in request.POST and request.POST['action'] == 'remove_from_wishlist':
                book_id = request.POST['book_id']
                wishlist = Wishlist.objects.get(user=request.user)
                book_to_remove = Book.objects.get(id=book_id)
                wishlist.books.remove(book_to_remove)

        if request.method == 'POST':
            if 'action' in request.POST and request.POST['action'] == 'remove_from_notifications':
                notification_id = request.POST['notification_id']
                try:
                    notification_to_remove = Notification.objects.get(id=notification_id, recipient=request.user)
                    notification_to_remove.delete()
                except Notification.DoesNotExist:
                    return redirect('invalid_form')
        return redirect('user_profile')

class OtherUserProfileView(View):
    def get(self, request, user_id):
        other_user_profile = get_object_or_404(UserProfile, user__id=user_id)
        # Download information about user wanted to visit
        user_to_display = other_user_profile.user

        wishlist, created = Wishlist.objects.get_or_create(user=user_to_display)
        books_in_wishlist = wishlist.books.all()
        wishlist_form = WishlistForm()
        currently_reading_form = CurrentlyReadingForm(instance=other_user_profile)

        return render(request, 'bookstore_app/other_user_profile.html', {
            'user_to_display': user_to_display,
            'books_in_wishlist': books_in_wishlist,
            'wishlist_form': wishlist_form,
            'user_profile': other_user_profile,
            'currently_reading_form': currently_reading_form,
        })


def remove_from_wishlist(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.books.remove(book)
        return redirect('user_profile')


class AddFriendView(View):
    def get(self, request):
        form = AddFriendForm()
        return render(request,
                      'bookstore_app/add_friend.html',
                      {'form': form})

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
                else:
                    return render(request, 'bookstore_app/user_add_self.html')

            except UserProfile.DoesNotExist:
                return redirect('bookstore_app/user_does_not_exists.html')

        return HttpResponseRedirect(request.path_info)


class FriendsListView(View):
    def get(self, request, *args, **kwargs):
        form = RemoveFriendForm()
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        friends = user_profile.friends.all()
        return render(request,
                      'bookstore_app/friends_list.html',
                      {'friends': friends})

def remove_from_friends_list(request, friend_id):
    #function for removing a user from the friends
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        the_friend = get_object_or_404(UserProfile, pk=friend_id)
        request.user.userprofile.friends.remove(the_friend)
        return redirect('list_of_friends')

class WishlistView(View):
    def get(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        books_in_wishlist = wishlist.books.all()
        form = WishlistForm()
        return render(request,
                      'bookstore_app/wishlist.html',
                      {'form': form, 'books_in_wishlist': books_in_wishlist})

    def post(self, request):
        form = WishlistForm(request.POST)
        if form.is_valid():
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            books_to_add = form.cleaned_data.get('books')
            wishlist.books.add(*books_to_add)
        else:
            raise
        return redirect('wishlist')

class BooksReadView(View):
    def get(self, request, *args, **kwargs):
        books_read, created = UserProfile.objects.get_or_create(user=request.user)
        books_in_list = books_read.books_read_list.all()
        form = UserBooksForm()
        return render(request,
                      'bookstore_app/books_read.html',
                      {'form': form,
                       'books_in_list': books_in_list})

    def post(self, request, *args, **kwargs):
        form = UserBooksForm(request.POST)
        if form.is_valid():
            books_read, created = UserProfile.objects.get_or_create(user=request.user)
            books_to_add = form.cleaned_data.get('books_read_list')
            if books_to_add:
                books_read.books_read_list.add(*books_to_add)
            return redirect('read_books')
        return render(request,
                      'bookstore_app/books_read.html',
                      {'form': form, 'books_in_list': books_in_list})


def search_for_book(request):
    query_title = request.GET.get('title')
    query_author = request.GET.get('author')
    query_genre = request.GET.get('genre')

    books = Book.objects.all()
    if query_title:
        books = books.filter(title__icontains=query_title)
    if query_author:
        books = books.filter(author__icontains=query_author)
    if query_genre:
        books = books.filter(genre__icontains=query_genre)

    return render(request,
                  'bookstore_app/search_for_book.html',
                  {'books': books})


# class FriendProfileView(DetailView):
#     model = UserProfile
#     template_name = 'bookstore_app/friends_list.html'
#     context_object_name = 'friend_profile'


