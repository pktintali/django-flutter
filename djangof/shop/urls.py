from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('miscards',MisCardViewSet)
router.register('users',UserViewSet)

miscard_router = routers.NestedDefaultRouter(router, 'miscards', lookup='miscard')
miscard_router.register('comments', CommentViewSet, basename='miscard-comments')

urlpatterns = [ 
    path('products/', ProductView.as_view()),
    path('favorit/', FavoritView.as_view()),
    path('login/', obtain_auth_token),
    path('register/', RegisterView.as_view()),
    path('cart/', CartView.as_view()),
    path('order/', OrderView.as_view()),
    path('addtocart/', AddToCart.as_view()),
    path('delatecartprod/', DelateCarProduct.as_view()),
    path('deletecart/', DelateCart.as_view()),
    path('ordernow/', OrderCreate.as_view()),
]+router.urls+miscard_router.urls
# /api/
