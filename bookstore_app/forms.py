from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Wishlist, Book, UserProfile


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name',
                  'email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class FriendsListForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['books']

class AddFriendForm(forms.Form):
    friend_username = forms.CharField(label='Username of Friend')

class UserRatingForm(forms.Form):
    like = forms.CharField(required=False, widget=forms.HiddenInput(), initial="like")
    dislike = forms.CharField(required=False, widget=forms.HiddenInput(), initial="dislike")
    add_wishlist = forms.CharField(widget=forms.HiddenInput(), initial="add_wishlist")
    user_has_rated = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=False)

class UserBooksForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['books_read_list']


class CurrentlyReadingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['currently_reading_book']
