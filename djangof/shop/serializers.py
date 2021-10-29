from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user, get_user_model
from rest_framework.authtoken.models import Token
#dependency
from core.models import User
from django.conf import settings


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


# User = get_user_model()


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'email',)
        extra_kwargs = {'password': {"write_only": True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"
        depth = 1


class OrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name']
class MisCardSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    #TODO Handle Select Related 
    class Meta:
        model = MisCard
        fields = ['id','created_at','title','mistake','lesson','user']

class MisCardAddSerializer(serializers.ModelSerializer):
    #TODO Handle Select Related 
    class Meta:
        model = MisCard
        fields = ['id','created_at','title','mistake','lesson']
    
    def create(self, validated_data):
        user = self.context['user']
        return MisCard.objects.create(user=user,**validated_data)



# class SimpleCommentUserSirializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','username','first_name','last_name']
class CommentSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer()
    class Meta:
        model = Comment
        fields = ['id','description','created_at','miscard_id','user']
    
    def create(self, validated_data):
        miscard_id = self.context['miscard_id']
        return Comment.objects.create(miscard_id=miscard_id, **validated_data)

class CommentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','description','created_at','miscard_id']
    
    def create(self, validated_data):
        miscard_id = self.context['miscard_id']
        user_id = self.context['user_id']
        return Comment.objects.create(miscard_id=miscard_id,user_id=user_id, **validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','first_name','last_name','email']