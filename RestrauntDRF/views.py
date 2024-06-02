from rest_framework import generics
from .models import *
from .serializer import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes,api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from Users.models import CustomUser as User
from Users.serializers import CustomUserSerializer

class Add_Categories_View(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    

class Edit_Categories_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    
class MenuItemsView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price','inventory']
    filterset_fields = ['price','title','category']
    search_fields = ['title']
    

class MenuItemView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_object(self):
        item = self.kwargs['title']
        return get_object_or_404(MenuItem, title=item)
    def list(self,request,*args, **kwargs):
        isinstance = self.get_object()
        
    
class Add_MenuItems_View(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]
    ordering_fields=['price','inventory']
    filterset_fields = ['price','title']
    search_fields = ['title']

class Edit_MenuItem_View(generics.RetrieveUpdateDestroyAPIView):
        queryset = MenuItem.objects.all()
        serializer_class = MenuItemSerializer
        permission_classes = [IsAdminUser]

class order(generics.CreateAPIView):
        queryset = order_list.objects.all()
        serializer_class = orderserializer
        permission_classes = [IsAuthenticated]
        
        def perform_create(self, serializer):
            owner = self.request.user
            order = self.kwargs['title']
        
            try:
                menu_item = MenuItem.objects.get(title=order)
            except MenuItem.DoesNotExist:
                raise NotFound(f"MenuItem with id {order} does not exist")
        
            serializer.save(owner=owner, order=menu_item)

class list_order(generics.ListAPIView):
        queryset = order_list.objects.all()
        serializer_class = orderserializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
            owner = self.request.user
            return order_list.objects.filter(owner=owner)
        def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            if not queryset.exists():
                return Response({"detail": "No items in your cart"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
             
        


class update_order(generics.RetrieveUpdateDestroyAPIView):
        queryset = order_list.objects.all()
        serializer_class = orderserializer
        permission_classes = [IsAuthenticated]    
            
        

class order_adminlist(generics.ListCreateAPIView):
        queryset = order_list.objects.all()
        serializer_class = orderserializer
        permission_classes = [IsAdminUser]
        ordering_fields=['time']
        filterset_fields = ['order']
        
        
class order_item(generics.RetrieveDestroyAPIView):
        queryset = order_list.objects.all()
        serializer_class = orderserializer
        permission_classes = [IsAdminUser]
        

        

        
        
class Cart_add(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        owner = self.request.user
        item = self.kwargs['title']
        try : 
             menu_item = MenuItem.objects.get(title=item) 
        except MenuItem.DoesNotExist:
                raise NotFound(f"MenuItem with id {item} does not exist")
        if Cart.objects.filter(owner=owner,item=menu_item).exists():
            return Response({"detial":"you have already added it to your cart"},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(owner=owner, item=menu_item)
            
            
class Cart_list(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        owner = self.request.user
        return Cart.objects.filter(owner=owner)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No items in your cart"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class Cart_delete(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        owner = self.request.user
        item = self.kwargs['title']
        menu_item = get_object_or_404(MenuItem,title=item)
        return get_object_or_404(Cart, owner=owner, item_id=menu_item)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
class Like(generics.CreateAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikeSerializers
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        item = self.kwargs['title']
        try:
            menu_item = MenuItem.objects.get(title=item)
        except MenuItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if Likes.objects.filter(user=user,item=menu_item).exists():
            return Response({"detial":"you have already liked it"},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(user=user, item=menu_item)

class Like_list(generics.ListAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikeSerializers
    
    def get_queryset(self):
        item = self.kwargs['title']
        try:
            menu_item =  MenuItem.objects.get(title=item)
        except MenuItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Likes.objects.filter(item=menu_item)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count() 
        if not queryset.exists():
            return Response('no likes for this item',status=status.HTTP_404_NOT_FOUND)
        if count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset,many=True)
        
        data = {'count': count,
                'data':serializer.data}
        serializer = LikeCountSerializer(data)
        return Response(serializer.data)
    

class like_delete(generics.RetrieveDestroyAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikeSerializers
    

class Comment(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        item = self.kwargs['title']
        
        try:
            menu_item = MenuItem.objects.get(title=item)
        except MenuItem.DoesNotExist:
            return Response('no item',status=status.HTTP_404_NOT_FOUND)
        serializer.save(user=user,item=menu_item)
        return Response('commented',status=status.HTTP_200_OK)


class Comment_List(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        item = self.kwargs['title']
        menu_itme = MenuItem.objects.get(title=item)
        return Comments.objects.filter(item=menu_itme)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        if count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset,many=True)
        data = {'count':count,
                'data':serializer.data
        }
        serializer = CommentsCountSerializer(data)
        return Response(serializer.data)

class Edit_Comment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        item = self.kwargs['title']
        id = self.kwargs['id']
        menu_itme = MenuItem.objects.get(title=item)
        return get_object_or_404(Comments,item=menu_itme,user=user,id=id)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        comment_instance = self.get_object()
        serializer = self.get_serializer(comment_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        queryset = self.get_object()
        removed_item = queryset.delete()
        return Response('comment is deleted',status=status.HTTP_404_NOT_FOUND)

        
    
    