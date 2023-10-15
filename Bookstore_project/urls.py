from django.contrib import admin
from django.urls import path
from bookstore_app import views as bk_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', bk_views.RegistrationView.as_view(), name='registration'),
    path('login/', bk_views.LoginView.as_view(), name='login'),
]
