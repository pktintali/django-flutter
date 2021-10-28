from django.contrib import admin
from .models import Cart, MisCard, Product, CartProduct, Category, Order, Favorire


admin.site.register([Cart, Product, CartProduct, Category, Order, Favorire,MisCard ])
