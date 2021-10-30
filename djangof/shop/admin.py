from django.contrib import admin
from .models import *


admin.site.register([Profile,Followings,Cart, Product, CartProduct, Category, Order, Favorire,MisCard,Comment,Like,DisLike ])
