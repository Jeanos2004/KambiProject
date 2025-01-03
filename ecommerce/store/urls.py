from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ProfileUpdateView, delivery_dashboard

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.custom_signup, name='signup'),
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('order/history/', views.order_history, name='order_history'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('delivery_persons/', views.delivery_person_list, name='delivery_person_list'),
    path('delivery_persons/add/', views.add_delivery_person, name='add_delivery_person'),
    path('delivery_persons/update/<int:pk>/', views.update_delivery_person, name='update_delivery_person'),
    path('orders/<int:order_id>/assign_delivery_person/', views.assign_delivery_person, name='assign_delivery_person'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('delivery/dashboard/', delivery_dashboard, name='delivery_dashboard'),
]
