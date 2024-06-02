from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from Users.serializers import CustomUserSerializer,UserSerializer
from Users.models import CustomUser as User




class userseriazizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name']

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']
        

class MenuItemSerializer(serializers.ModelSerializer):
     category_id = serializers.IntegerField(write_only=True)
     category = CategorySerializer(read_only=True)
     class Meta:
         model = MenuItem
         fields = ['id', 'title', 'price', 'inventory', 'category' ,'category_id']
        #  lookup_field = 'title'
        

class orderserializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    order = MenuItemSerializer(read_only=True)
    class Meta:
        model = order_list
        fields = ['id','order','time','owner','phone','useraddress','quantity','email']
        
class CartSerializers(serializers.ModelSerializer):
    item = MenuItemSerializer(read_only=True)
    owner = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id','item','owner']
        
        
class LikeSerializers(serializers.ModelSerializer):
    item = MenuItemSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Likes
        fields = ['id','item','user']
        
class LikeCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    data = LikeSerializers(many=True)
    
class CommentSerializer(serializers.ModelSerializer):
    user =CustomUserSerializer(read_only=True)
    item = MenuItemSerializer(read_only=True)
    
    class Meta:
        model = Comments
        fields = ['id','comment','user','item']
        
class CommentsCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    data = CommentSerializer(many=True)
    
