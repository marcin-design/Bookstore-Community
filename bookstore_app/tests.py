from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from django.test import RequestFactory
from django.test import Client

from bookstore_app.models import UserProfile
from bookstore_app.views import RegistrationView, search_for_book, FriendsListView, logout_view
import pytest

User = get_user_model()
# access to the user model
def test_get_registration_view():
    factory = RequestFactory()
    # tool for creating HTTP request objects
    request = factory.get(reverse('registration'))
    # creates an HTTP GET request object for the "registration" view
    # using the reverse function, which generates a URL based on the view name
    response = RegistrationView.as_view()(request)
    # simulates a RegistrationView call using as_view()
    # this returns the response that is generated by this view
    assert response.status_code == 200
    assert b'registration' in response.content
    # check whether the phrase 'registration' appears in the content of the response


@pytest.mark.django_db
def test_post_invalid_registration_view():
    factory = RequestFactory()
    # tool for creating HTTP request objects
    data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'mismatchedpassword',
        # Mismatched password
    }
    request = factory.post(reverse('registration'), data)
    # creates an HTTP GET request object for the "registration" view
    # using the reverse function, which generates a URL based on the view name
    response = RegistrationView.as_view()(request)
    # simulates a RegistrationView call using as_view()
    # this returns the response that is generated by this view
    assert response.status_code == 200
    assert b'registration' in response.content
    assert b'Incorrect_registration' in response.content
    # check whether the phrase 'Incorrect_registration' appears in the content of the response


@pytest.mark.django_db
def test_logout_view():
    client = Client()
    # creating a user
    user = User.objects.create_user(username='testuser', password='testpassword')
    # logining in a user
    client.login(username='testuser', password='testpassword')
    # triggering logout_view
    response = client.get(reverse('logout'))
    # checking if a user is logged out
    assert response.context['user'].is_anonymous