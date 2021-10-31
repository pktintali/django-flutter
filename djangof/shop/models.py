from django.db import models
from django.conf import settings
from django.db.models.base import Model

class Category(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    data = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    marcket_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Favorire(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.Case)
    isFavorit = models.BooleanField(default=False)

    def __str__(self):
        return f"productID ={self.product.id}user={self.user.username}|ISFavorite={self.isFavorit}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    isComplit = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User={self.user.username}|ISComplit={self.isComplit}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Qualtity=={self.quantity}"


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=200)


class MisCard(models.Model):
    title = models.CharField(max_length=255)
    mistake = models.TextField()
    lesson = models.TextField()
    comment_allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.title[:25]+'...'


class Comment(models.Model):
    miscard = models.ForeignKey(MisCard,on_delete=models.CASCADE,related_name='comments')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class Like(models.Model):
    miscard = models.ForeignKey(MisCard,on_delete=models.CASCADE,related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('miscard','user')

class DisLike(models.Model):
    miscard = models.ForeignKey(MisCard,on_delete=models.CASCADE,related_name='dislikes')
    disliked_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('miscard','user')

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='comment_likes')
    liked_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('comment','user')

class CommentDisLike(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='comment_dislikes')
    disliked_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('comment','user')
    
class SavedMisCard(models.Model):
    miscard = models.ForeignKey(MisCard,on_delete=models.CASCADE,related_name='saved_miscards')
    saved_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('miscard','user')

class Profile(models.Model):
    banner = models.ImageField(upload_to="banners/")
    profile_pic = models.ImageField(upload_to="profile_pics/")
    dob = models.DateField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    about = models.TextField()
    impactor_badge = models.BooleanField(default=False)
    admin_badge = models.BooleanField(default=False)
    helper_badge = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class Followings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user')
    follow_time = models.DateField(auto_now_add=True)
    followed_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='followed_by')
    class Meta:
        unique_together = ('user','followed_by')

class Draft(models.Model):
    title = models.CharField(max_length=255)
    mistake = models.TextField()
    lesson = models.TextField()
    saved_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='draft_user')
