from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.utils import timezone



class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email required")
        if not password:
            raise ValueError("Password required")

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
    category = models.CharField(unique=True, max_length=30, primary_key=True)
    def __str__(self):
        return self.category


class Item(models.Model):
    STATUS = [('1', 'Available'), ('2', 'Payment Due'),
              ('3', 'Payment Complete'), ('4', 'Delivered')]
    CONDITION_CHOICES = [
        ('1', 'Fair'),
        ('2', 'Good'),
        ('3', 'Very Good'),
        ('4', 'Great'),
        ('5', 'Excellent'),
        ('6', 'Pristine'),
    ]
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    condition = models.CharField(
        max_length=1, choices=CONDITION_CHOICES, default="1")
    slug = models.SlugField(blank=True, null=True)
    base_price = models.IntegerField(default=0.0)
    current_price = models.IntegerField(default=0.0)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='items_to_sell')
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='items_bought')
    shipping_address = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS, default="1", max_length=20)

    def __str__(self):
        return self.item_name

    @property
    def auction_status(self):
        today = timezone.now()
        auction = self.auction
        if auction.cap_time < today:
            return "past"
        elif auction.start > today:
            return "upcoming"
        else:
            return "live" 
    
    def time_to_end(self):
        today = timezone.now()
        auction = self.auction
        if auction.cap_time < today:
            return 0
        else:
            return (auction.cap_time - today).total_seconds()

    
    def time_to_start(self):
        today = timezone.now()
        auction = self.auction
        if auction.cap_time < today:
            return 0
        else:
            return (today - auction.start_time).total_seconds()


class Image(models.Model):
    image = models.ImageField(
        default='item_images/itemimage.jpg', upload_to='item_images')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="item_images")


class Auction(models.Model):
    start =  models.DateTimeField(auto_now=False)
    item = models.OneToOneField(
        Item, on_delete=models.CASCADE, related_name="auction")
    cap_time =  models.DateTimeField(auto_now=False)


class Message(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auction")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.first_name + str(self.price)


class CustomerCare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()

#############
# RECEIVERS #
#############


def create_slug(instance, new_slug=None):
    slug = slugify(instance.item_name)
    if new_slug is not None:
        slug = new_slug
    qs = Item.objects.filter(slug=slug).order_by("id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Item)
def pre_save_item_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if kwargs.get("created"):
        instance.current_price = instance.base_price


@receiver(pre_save, sender=Message)
def pre_save_current_price_updater(sender, instance, *args, **kwargs):
    item = instance.auction.item
    item.current_price = instance.price
    item.save()
