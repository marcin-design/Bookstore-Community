from django.contrib import admin
from django.urls import path, include
from bookstore_app import views as bk_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', bk_views.RegistrationView.as_view(), name='registration'),
    path('login/', bk_views.LoginView.as_view(), name='login'),
    path('main/', bk_views.main_page, name='main'),
    path('logout/', bk_views.logout_view, name='logout'),
    path('user_profile/', bk_views.UserProfileView.as_view(), name='user_profile'),
    path('other_user_profile/<int:user_id>/', bk_views.OtherUserProfileView.as_view(), name='other_user_profile'),
    path('add_friend/', bk_views.AddFriendView.as_view(), name='add_friend'),
    path('friends_list/', bk_views.FriendsListView.as_view(), name='list_of_friends'),
    path('remove_friend/<int:friend_id>/', bk_views.remove_from_friends_list, name='remove_friend'),
    path('wishlist/', bk_views.WishlistView.as_view(), name='wishlist'),
    path('book_details/<book_id>/', bk_views.BookDetailsView.as_view(), name='book_details'),
    path('read_books/', bk_views.BooksReadView.as_view(), name='read_books'),
    path('search_book/', bk_views.search_for_book, name='query'),
    path('invalid_form/', bk_views.InvalidFormView.as_view(), name='invalid_form'),
    # path('avatar/', bk_views.AvatarView.as_view(), name='avatar'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)