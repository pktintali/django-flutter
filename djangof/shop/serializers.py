from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user, get_user_model
from rest_framework.authtoken.models import Token
#dependency
from core.models import User
from django.db import IntegrityError


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
    class Meta:
        model = MisCard
        fields = ['id','created_at','title','mistake','lesson','comment_allowed','likes_count','dislikes_count','user',]
    
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
class MisCardAddSerializer(serializers.ModelSerializer): 
    class Meta:
        model = MisCard
        fields = ['id','created_at','title','mistake','lesson','comment_allowed']
    def create(self, validated_data):
        user = self.context['user']
        return MisCard.objects.create(user=user,**validated_data)

class CommentSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer()
    class Meta:
        model = Comment
        fields = ['id','description','created_at','miscard_id','user','likes_count','dislikes_count']
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
class CommentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','description','created_at','miscard_id']
    
    def create(self, validated_data):
        miscard_id = self.context['miscard_id']
        user_id = self.context['user_id']
        return Comment.objects.create(miscard_id=miscard_id,user_id=user_id, **validated_data)

class LikeSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer()
    class Meta:
        model = Like
        fields = ['id','liked_at','miscard_id','user']
class LikeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','liked_at','miscard_id']

    def create(self, validated_data):
        miscard_id = self.context['miscard_id']
        user_id = self.context['user_id']
        if DisLike.objects.filter(user_id=user_id,miscard_id=miscard_id).exists():
            DisLike.objects.filter(user_id=user_id,miscard_id=miscard_id).delete()
        try:
            return Like.objects.create(miscard_id=miscard_id,user_id=user_id, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Can\'t like same card more than once')
class DisLikeSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer()
    class Meta:
        model = DisLike
        fields = ['id','disliked_at','miscard_id','user']
class DisLikeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ['id','disliked_at','miscard_id']

    def create(self, validated_data):
        miscard_id = self.context['miscard_id']
        user_id = self.context['user_id']
        if Like.objects.filter(user_id=user_id,miscard_id=miscard_id).exists():
            Like.objects.filter(user_id=user_id,miscard_id=miscard_id).delete()
        try:
            return DisLike.objects.create(miscard_id=miscard_id,user_id=user_id, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Can\'t dislike same card more than once')
class CommentLikeSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer()
    class Meta:
        model = CommentLike
        fields = ['id','liked_at','comment_id','user']
class CommentLikeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['id','liked_at','comment_id']

    def create(self, validated_data):
        comment_id = self.context['comment_id']
        user_id = self.context['user_id']
        if CommentDisLike.objects.filter(user_id=user_id,comment_id=comment_id).exists():
            CommentDisLike.objects.filter(user_id=user_id,comment_id=comment_id).delete()
        try:
            return CommentLike.objects.create(comment_id=comment_id,user_id=user_id, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Can\'t like same comment more than once')
class CommentDisLikeSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer()
    class Meta:
        model = CommentDisLike
        fields = ['id','disliked_at','comment_id','user']
class CommentDisLikeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentDisLike
        fields = ['id','disliked_at','comment_id']

    def create(self, validated_data):
        comment_id = self.context['comment_id']
        user_id = self.context['user_id']
        if CommentLike.objects.filter(user_id=user_id,comment_id=comment_id).exists():
            CommentLike.objects.filter(user_id=user_id,comment_id=comment_id).delete()
        try:
            return CommentDisLike.objects.create(comment_id=comment_id,user_id=user_id, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Can\'t dislike same card more than once')
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','date_joined']
class UserAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','first_name','last_name','email']

class SimpleMisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MisCard
        fields = ['id','created_at','title','mistake','lesson']

class AllLikeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    miscard = SimpleMisCardSerializer()
    class Meta:
        model = Like
        fields = ['id','user','miscard']
class AllDisLikeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    miscard = SimpleMisCardSerializer()
    class Meta:
        model = DisLike
        fields = ['id','user','miscard']
class AllCommentsSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    miscard = SimpleMisCardSerializer()
    class Meta:
        model = Comment
        fields = ['id','miscard','description','user','created_at']
class CreatorSimpleLikesSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    class Meta:
        model = User
        fields = ['user']
class CreatorLikesSerializer(serializers.ModelSerializer):
    miscard = CreatorSimpleLikesSerializer()
    class Meta:
        model = Like
        fields = ['id','miscard','user']
class SavedMisCardsSerializer(serializers.ModelSerializer):
    miscard = SimpleMisCardSerializer()
    class Meta:
        model = SavedMisCard
        fields = ['id','user','miscard']
class SavedMisCardsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedMisCard
        fields = ['id','miscard']
    
    def create(self, validated_data):
        user = self.context['user']
        try:
            return SavedMisCard.objects.create(user=user,**validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Can\'t save same card more than once')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','banner','profile_pic','dob','verified','about','impactor_badge','admin_badge','helper_badge']
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        return Profile.objects.create(user_id=user_id, **validated_data)

class FollowingsSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer()
    followed_by = SimpleUserSerializer()
    class Meta:
        model = Followings
        fields = ['id','user','followed_by','follow_time']
class FollowingsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followings
        fields = ['id','user','follow_time']

    def create(self, validated_data):
        followed_by = self.context['user_id']
        return Followings.objects.create(followed_by=followed_by,**validated_data)

class DraftSerializer(serializers.ModelSerializer):
    #TODO Handle Select Related 
    class Meta:
        model = Draft
        fields = ['id','saved_at','title','mistake','lesson']
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        return Draft.objects.create(user_id=user_id,**validated_data)