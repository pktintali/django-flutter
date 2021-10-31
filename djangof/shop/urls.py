from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('miscards',MisCardViewSet,basename='miscards')
router.register('users',UserViewSet)
router.register('currentuser',CurrentUserViewSet,basename='currentuser')
router.register('likes',AllLikesViewSet,basename='likes')
router.register('dislikes',AllDisLikesViewSet,basename='dislikes')
router.register('comments',AllCommentsViewSet,basename='comments')
router.register('saved_miscards',SavedMisCardsViewSet,basename='saved_miscards')
router.register('followings',FollowingsViewSet,basename='followings')

miscard_router = routers.NestedDefaultRouter(router, 'miscards', lookup='miscard')
miscard_router.register('comments', CommentViewSet, basename='miscard-comments')
miscard_router.register('likes', LikeViewSet, basename='miscard-likes')
miscard_router.register('dislikes', DisLikeViewSet, basename='miscard-dislikes')

comment_router = routers.NestedDefaultRouter(miscard_router, 'comments', lookup='comment')
comment_router.register('likes',CommentLikeViewSet,basename='comment-likes')
comment_router.register('dislikes',CommentDisLikeViewSet,basename='comment-dislikes')

profile_router = routers.NestedDefaultRouter(router, 'users', lookup='user')
profile_router.register('profile',ProfileViewSet,basename='profiles')
profile_router.register('drafts',DraftViewSet,basename='drafts')

current_user_profile_router = routers.NestedDefaultRouter(router, 'currentuser', lookup='user')
current_user_profile_router.register('profile',ProfileViewSet,basename='profiles')
current_user_profile_router.register('drafts',DraftViewSet,basename='drafts')

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
    path('creatorlikes/',CreatorLikeView.as_view()),
]+router.urls+miscard_router.urls+comment_router.urls+profile_router.urls+current_user_profile_router.urls
# /api/
