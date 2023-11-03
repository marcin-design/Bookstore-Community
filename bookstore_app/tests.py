import pytest
import unittest
import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_friends_list_view_get():
    user = User.objects.create_user(username="testuser", password="testpassword")
