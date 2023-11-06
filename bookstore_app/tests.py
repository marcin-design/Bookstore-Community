from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory

from bookstore_app.views import RegistrationView
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
