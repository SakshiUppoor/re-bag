from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email required")
        if not password:
            raise ValuError("Password required")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    image = models.ImageField(
        default='profile_images/profilepic.jpg', upload_to='profile_images')
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,10}$", message="Phone number must be valid"
    )
    phone = models.CharField(
        validators=[phone_regex], max_length=10
    )
    address = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Category(models.Model):
    category = models.CharField(unique=True, max_length=30)


class Subcategory(models.Model):
    subcategory = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Item(models.Model):
    STATUS = [('1', 'Available'), ('2', 'Payment Due'),
              ('3', 'Payment Complete'), ('4', 'Delivered')]
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    slug = models.SlugField()
    base_price = models.FloatField(default=0.0)
    current_price = models.FloatField(default=0.0)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='seller')
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='buyer')
    shipping_address = models.TextField()
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default="1", max_length=20)


class Image(models.Model):
    image = models.ImageField(
        default='item_images/itemimage.jpg', upload_to='item_images')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Auction(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    cap_time = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    anon_name = models.CharField(max_length=20)
    raised_by = models.FloatField(default=0)
    time_stamp = models.DateTimeField(auto_now_add=True)


class CustomerCare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
