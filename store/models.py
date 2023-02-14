from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='store/images', default='store/images/default.png')

    def __str__(self):
        return self.name


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=250)
    price = models.FloatField(default=0.0)
    price_origin = models.FloatField(null=True)
    image = models.ImageField(upload_to='store/images', default='store/images/default.png')
    content = RichTextUploadingField(blank=True, null=True)
    public_day = models.DateTimeField(default=timezone.now)
    viewed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-public_day',)


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True)
    subject = models.CharField(max_length=264)
    message = models.TextField()

    def __str__(self):
        return self.subject


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    portfolio = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='users/', default='users/no_avatar.jpg')

    def __str__(self):
        return self.user.username

    #định nghĩa lại tên table trong DB
    class Meta:
        db_table = u'userprofileinfo'