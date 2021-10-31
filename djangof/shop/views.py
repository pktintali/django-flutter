from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.db.models.aggregates import Count
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter,OrderingFilter
from shop.pagination import DefaultPagination
from .serializers import *
from .models import *
class ProductView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        query = Product.objects.all()
        data = []
        serializers = ProductSerializer(query, many=True)
        for product in serializers.data:
            fab_query = Favorire.objects.filter(
                user=request.user).filter(product_id=product['id'])
            if fab_query:
                product['favorit'] = fab_query[0].isFavorit
            else:
                product['favorit'] = False
            data.append(product)
        return Response(data)


class FavoritView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        data = request.data["id"]
        # print(data)
        try:
            product_obj = Product.objects.get(id=data)
            # print(data)
            user = request.user
            single_favorit_product = Favorire.objects.filter(
                user=user).filter(product=product_obj).first()
            if single_favorit_product:
                print("single_favorit_product")
                ccc = single_favorit_product.isFavorit
                single_favorit_product.isFavorit = not ccc
                single_favorit_product.save()
            else:
                Favorire.objects.create(
                    product=product_obj, user=user, isFavorit=True)
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class RegisterView(APIView):
    def post(self, request):
        serializers = Userserializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"error": False})
        return Response({"error": True})


class CartView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user
        try:
            cart_obj = Cart.objects.filter(user=user).filter(isComplit=False)
            data = []
            cart_serializer = CartSerializers(cart_obj, many=True)
            for cart in cart_serializer.data:
                cart_product_obj = CartProduct.objects.filter(cart=cart["id"])
                cart_product_obj_serializer = CartProductSerializers(
                    cart_product_obj, many=True)
                cart['cartproducts'] = cart_product_obj_serializer.data
                data.append(cart)
            response_msg = {"error": False, "data": data}
        except:
            response_msg = {"error": True, "data": "No Data"}
        return Response(response_msg)


class OrderView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        try:
            query = Order.objects.filter(cart__user=request.user)
            serializers = OrdersSerializers(query, many=True)
            response_msg = {"error": False, "data": serializers.data}
        except:
            response_msg = {"error": True, "data": "no data"}
        return Response(response_msg)


class AddToCart(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(sefl, request):
        product_id = request.data['id']
        product_obj = Product.objects.get(id=product_id)
        # print(product_obj, "product_obj")
        cart_cart = Cart.objects.filter(
            user=request.user).filter(isComplit=False).first()
        cart_product_obj = CartProduct.objects.filter(
            product__id=product_id).first()

        try:
            if cart_cart:
                print(cart_cart)
                print("OLD CART")
                this_product_in_cart = cart_cart.cartproduct_set.filter(
                    product=product_obj)
                if this_product_in_cart.exists():
                    cartprod_uct = CartProduct.objects.filter(
                        product=product_obj).filter(cart__isComplit=False).first()
                    cartprod_uct.quantity += 1
                    cartprod_uct.subtotal += product_obj.selling_price
                    cartprod_uct.save()
                    cart_cart.total += product_obj.selling_price
                    cart_cart.save()
                else:
                    print("NEW CART PRODUCT CREATED--OLD CART")
                    cart_product_new = CartProduct.objects.create(
                        cart=cart_cart,
                        price=product_obj.selling_price,
                        quantity=1,
                        subtotal=product_obj.selling_price
                    )
                    cart_product_new.product.add(product_obj)
                    cart_cart.total += product_obj.selling_price
                    cart_cart.save()
            else:
                Cart.objects.create(user=request.user,
                                    total=0, isComplit=False)
                new_cart = Cart.objects.filter(
                    user=request.user).filter(isComplit=False).first()
                cart_product_new = CartProduct.objects.create(
                    cart=new_cart,
                    price=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price
                )
                cart_product_new.product.add(product_obj)
                new_cart.total += product_obj.selling_price
                new_cart.save()
            response_mesage = {
                'error': False, 'message': "Product add to card successfully", "productid": product_id}
        except:
            response_mesage = {'error': True,
                               'message': "Product Not add!Somthing is Wromg"}
        return Response(response_mesage)


class DelateCarProduct(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        cart_product_id = request.data['id']
        try:
            cart_product_obj = CartProduct.objects.get(id=cart_product_id)
            cart_cart = Cart.objects.filter(
                user=request.user).filter(isComplit=False).first()
            cart_cart.total -= cart_product_obj.subtotal
            cart_product_obj.delete()
            cart_cart.save()
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class DelateCart(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        cart_id = request.data['id']
        try:
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.delete()
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class OrderCreate(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def post(self, request):
        try:
            data = request.data
            cart_id = data['cartid']
            address = data['address']
            email = data['email']
            phone = data['phone']
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.isComplit = True
            cart_obj.save()
            Order.objects.create(
                cart=cart_obj,
                email=email,
                address=address,
                phone=phone,
            )
            response_msg = {"error": False, "message": "Your Order is Complit"}
        except:
            response_msg = {"error": True, "message": "Somthing is Wrong !"}
        return Response(response_msg)


class MisCardViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [TokenAuthentication, ]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['user_id']
    search_fields = ['title','mistake','lesson','user__username','user__first_name']
    ordering_fields = ['created_at','likes_count','dislikes_count']
    queryset = MisCard.objects.select_related('user')\
    .annotate(likes_count=Count('likes'))\
    .annotate(dislikes_count=Count('dislikes'))\
    .order_by('id').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MisCardSerializer
        else:
            return MisCardAddSerializer
    
    def get_serializer_context(self):
        return {'user':self.request.user}
    

class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [TokenAuthentication, ]
    pagination_class = DefaultPagination
    filter_backends = [OrderingFilter]
    ordering_fields= ['created_at','likes_count','dislikes_count']
    def get_serializer_class(self):
        if self.request.method=='GET':
            return CommentSerializer
        else:
            return CommentAddSerializer

    def get_queryset(self):\
        return Comment.objects\
                      .annotate(likes_count=Count('comment_likes'),dislikes_count=Count('comment_dislikes'))\
                      .filter(miscard_id=self.kwargs['miscard_pk'])\
                      .select_related('user')\
                      .all()
    
    def get_serializer_context(self):
        return {'miscard_id': self.kwargs['miscard_pk'],'user_id':self.request.user.id}
class LikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [TokenAuthentication, ]
    pagination_class = DefaultPagination
    filter_backends = [OrderingFilter]
    ordering_fields= ['liked_at']
    def get_serializer_class(self):
        if self.request.method=='GET':
            return LikeSerializer
        else:
            return LikeAddSerializer
    def get_queryset(self):\
        return Like.objects\
                      .filter(miscard_id=self.kwargs['miscard_pk'])\
                      .select_related('user')\
                      .order_by('id')\
                      .all()
    
    def get_serializer_context(self):
        return {'miscard_id': self.kwargs['miscard_pk'],'user_id':self.request.user.id}
class DisLikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [TokenAuthentication, ]
    def get_serializer_class(self):
        if self.request.method=='GET':
            return DisLikeSerializer
        else:
            return DisLikeAddSerializer

    def get_queryset(self):\
        return DisLike.objects\
                      .filter(miscard_id=self.kwargs['miscard_pk'])\
                      .select_related('user')\
                      .all()
    
    def get_serializer_context(self):
        return {'miscard_id': self.kwargs['miscard_pk'],'user_id':self.request.user.id}
class CommentLikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [TokenAuthentication, ]
    def get_serializer_class(self):
        if self.request.method=='GET':
            return CommentLikeSerializer
        else:
            return CommentLikeAddSerializer

    def get_queryset(self):\
        return CommentLike.objects\
                      .filter(comment_id=self.kwargs['comment_pk'])\
                      .select_related('user')\
                      .all()
    
    def get_serializer_context(self):
        return {'comment_id': self.kwargs['comment_pk'],'user_id':self.request.user.id}
class CommentDisLikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [TokenAuthentication, ]
    def get_serializer_class(self):
        if self.request.method=='GET':
            return CommentDisLikeSerializer
        else:
            return CommentDisLikeAddSerializer

    def get_queryset(self):\
        return CommentDisLike.objects\
                      .filter(comment_id=self.kwargs['comment_pk'])\
                      .select_related('user')\
                      .all()
    
    def get_serializer_context(self):
        return {'comment_id': self.kwargs['comment_pk'],'user_id':self.request.user.id}


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['username','first_name','last_name']
    ordering_fields= ['date_joined','username','first_name']
    def get_serializer_class(self):
        if self.request.method=='GET':
            return  UserSerializer
        else:
            return UserAddSerializer
    queryset = User.objects.all()

class CurrentUserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    
    def get_serializer_class(self):
        if self.request.method=='GET':
            return  UserSerializer
        else:
            return UserAddSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)


class AllLikesViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['user_id','miscard_id']
    ordering_fields = ['liked_at']
    queryset = Like.objects.order_by('id').all()
    serializer_class = AllLikeSerializer
class AllDisLikesViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['user_id','miscard_id']
    ordering_fields = ['disliked_at']
    queryset = DisLike.objects.order_by('id').all()
    serializer_class = AllDisLikeSerializer
class AllCommentsViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['user_id','miscard_id']
    ordering_fields = ['created_at']
    queryset = Comment.objects.order_by('id').all()
    serializer_class = AllCommentsSerializer

class SavedMisCardsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['user_id','miscard_id']
    ordering_fields = ['saved_at','miscard__title']
    queryset = SavedMisCard.objects.select_related('miscard').order_by('id').all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SavedMisCardsSerializer
        else:
            return SavedMisCardsAddSerializer
    
    def get_serializer_context(self):
        return {'user':self.request.user}


class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer
    def get_queryset(self):\
        return Profile.objects\
                      .filter(user_id=self.kwargs['user_pk'])\
                      .select_related('user')\
                      .all()
    def get_serializer_context(self):
        return {'user_id': self.kwargs['user_pk']}


class FollowingsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['followed_by__username','followed_by__first_name','followed_by__last_name']
    filterset_fields = ['user_id','followed_by']
    ordering_fields = ['user__last_name','user__first_name','followed_by__username','followed_by__first_name','follow_time']
    queryset = Followings.objects.order_by('id').all()


    def get_serializer_class(self):
        if self.request.method=='GET':
            return FollowingsSerializer
        else:
            return FollowingsAddSerializer
    def get_serializer_context(self):
        return {'user_id': self.request.user}

class DraftViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [TokenAuthentication, ]
    pagination_class = DefaultPagination
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ['title']
    ordering_fields = ['saved_at']
    serializer_class = DraftSerializer

    def get_queryset(self):
        queryset = Draft.objects.select_related('user').filter(user_id=self.kwargs['user_pk']).order_by('id').all()
        return queryset

    def get_serializer_context(self):
        return {'user':self.request.user,'user_id': self.kwargs['user_pk'],}

    
class CreatorLikeView(APIView):
    # queryset = Like.objects.all()
    # serializer_class = CreatorLikesSerializer
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        query = Like.objects.all()
        total_likes = 0
        serializers = CreatorLikesSerializer(query, many=True)
        current_user_id = request.user.id
        for i in  serializers.data:
            creator_id = i['miscard']['user']['id']
            if creator_id==current_user_id:
                total_likes+=1
        return Response({'id':current_user_id,'total_likes':total_likes})

