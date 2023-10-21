from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.CharField(max_length=10, null=True, blank=True)
    genre = models.CharField(max_length=50)
    user_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    thumbnail = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    books_read_list = models.ManyToManyField(Book, related_name='read_by_user')
    current_book = models.ForeignKey(Book,
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='currently_reading')
    user_description = models.TextField(blank=True, null=True)
    has_access = models.BooleanField(default=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)

class Friendship(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_friendships')
    friend = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user} - {self.friend}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.user} - {self.book}"

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name='user_wishlist')

    def __str__(self):
        return f"Wishlist created by user {self.user}"
