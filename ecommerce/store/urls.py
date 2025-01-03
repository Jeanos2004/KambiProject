from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ProfileUpdateView, delivery_dashboard

urlpatterns = [
    # Route pour la page de connexion
    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    # Route pour le profil de l'utilisateur
    path('profile/', views.profile, name='profile'),
    
    # Route pour déconnexion de l'utilisateur
    path('logout/', views.custom_logout, name='logout'),
    
    # Route pour l'inscription d'un nouvel utilisateur
    path('signup/', views.custom_signup, name='signup'),
    
    # Route pour la page d'accueil
    path('', views.home, name='home'),
    
    # Route pour afficher la liste des produits
    path('products/', views.product_list, name='product_list'),
    
    # Route pour afficher le panier de l'utilisateur
    path('cart/', views.view_cart, name='view_cart'),
    
    # Route pour ajouter un produit au panier
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # Route pour supprimer un produit du panier
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Route pour mettre à jour la quantité d'un produit dans le panier
    path('cart/update/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
    
    # Route pour le processus de paiement
    path('checkout/', views.checkout, name='checkout'),
    
    # Route pour afficher les produits favoris de l'utilisateur
    path('favorites/', views.view_favorites, name='view_favorites'),
    
    # Route pour ajouter un produit aux favoris
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    
    # Route pour la suppression d'un element de la liste des favoris
    path('favorites/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    
    
    # Route pour ajouter un avis sur un produit
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    
    # Route pour afficher les détails d'un produit
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Route pour ajouter un avis sur un produit (doublon, à supprimer)
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    
    # Route pour afficher l'historique des commandes de l'utilisateur
    path('order/history/', views.order_history, name='order_history'),
    
    # Route pour afficher les notifications de l'utilisateur
    path('notifications/', views.notifications, name='notifications'),
    
    # Route pour marquer une notification comme lue
    path('notifications/read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    
    # Route pour afficher la liste des livreurs
    path('delivery_persons/', views.delivery_person_list, name='delivery_person_list'),
    
    # Route pour ajouter un nouveau livreur
    path('delivery_persons/add/', views.add_delivery_person, name='add_delivery_person'),
    
    # Route pour mettre à jour les informations d'un livreur
    path('delivery_persons/update/<int:pk>/', views.update_delivery_person, name='update_delivery_person'),
    
    # Route pour assigner un livreur à une commande
    path('orders/<int:order_id>/assign_delivery_person/', views.assign_delivery_person, name='assign_delivery_person'),
    
    # Route pour mettre à jour le profil de l'utilisateur
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    
    # Route pour afficher le tableau de bord de livraison
    path('delivery/dashboard/', delivery_dashboard, name='delivery_dashboard'),
]
