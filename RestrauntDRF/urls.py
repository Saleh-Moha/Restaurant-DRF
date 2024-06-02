from django.urls import path
from . import views

urlpatterns = [
    path('category/add', views.Add_Categories_View.as_view()),
    path('category/edit/<int:pk>', views.Edit_Categories_View.as_view()),
    path('menu-items/add', views.Add_MenuItems_View.as_view()),
    path('menu-items/edit/<int:pk>', views.Edit_MenuItem_View.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<slug:title>', views.MenuItemView.as_view()),
    path('menu-items/<slug:title>/order', views.order.as_view()),
    path('orders/<int:pk>', views.update_order.as_view()),
    path('orders', views.list_order.as_view()),
    path('orderlist', views.order_adminlist.as_view()),
    path('orderlist/<int:pk>', views.order_item.as_view()),
    path('menu-items/<slug:title>/add-to-cart', views.Cart_add.as_view()),
    path('cart', views.Cart_list.as_view()),
    path('cart/<slug:title>', views.Cart_delete.as_view(), name='cart-delete'),
    path('menu-items/<slug:title>/like', views.Like.as_view(),),
    path('menu-items/<slug:title>/likes-number', views.Like_list.as_view(),),
    path('menu-items/<slug:title>/comment', views.Comment.as_view(),),
    path('menu-items/<slug:title>/comment-number', views.Comment_List.as_view(),),
    path('menu-items/<slug:title>/comment-edit/<int:id>', views.Edit_Comment.as_view(),),
    path('likedelete/<int:pk>', views.like_delete.as_view(),),
]