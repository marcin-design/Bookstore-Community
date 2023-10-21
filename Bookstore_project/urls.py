from django.contrib import admin
from django.urls import path
from bookstore_app import views as bk_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', bk_views.RegistrationView.as_view(), name='registration'),
    path('login/', bk_views.LoginView.as_view(), name='login'),
    path('main/', bk_views.main_page, name='main'),
    path('logout/', bk_views.logout_view, name='logout'),
    path('user_profile/', bk_views.UserProfileView.as_view(), name='user_profile'),
    path('add_friend/', bk_views.AddFriendView.as_view(), name='add_friend'),
    path('friends_list/', bk_views.FriendsListView.as_view(), name='list_of_friends'),
    path('wishlist/', bk_views.WishlistView.as_view(), name='wishlist'),
    path('book_details/<str:book_id>/', bk_views.BookDetailsView.as_view(), name='book_details'),
]
