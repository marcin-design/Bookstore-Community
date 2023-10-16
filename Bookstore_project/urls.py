from django.contrib import admin
from django.urls import path
from bookstore_app import views as bk_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', bk_views.RegistrationView.as_view(), name='registration'),
    path('', bk_views.LoginView.as_view(), name='login'),
    path('main/', bk_views.main_page, name='main'),
    path('logout/', bk_views.logout_view, name='logout'),
    path('user_profile/', bk_views.user_view, name='user_profile'),
]
