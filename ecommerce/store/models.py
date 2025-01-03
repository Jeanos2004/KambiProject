from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now

# Modèle utilisateur personnalisé
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    favorites = models.ManyToManyField('Product', related_name='favorited_by', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Champ pour l'upload de la photo de profil

    groups = models.ManyToManyField(
        Group,
        related_name='store_user_groups',  # Nom unique pour éviter les conflits
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='store_user_permissions',  # Nom unique pour éviter les conflits
        blank=True,
    )

# Catégorie de produit
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name
class DeliveryPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_person')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
# Produit
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    image = models.ImageField(upload_to='product_images/')
    date_added = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Pourcentage de réduction

    def __str__(self):
        return self.name
    
    def price_with_discount(self):
        return self.price * (1 - self.discount)



class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # Note de 1 à 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
    
# Modèle pour le panier
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

# Modèle pour les éléments du panier
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} dans le panier de {self.cart.user.username}"

    
    def total_price(self):
        return self.product.price_with_discount() * self.quantity
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # Statut de la commande
    delivery_address = models.CharField(max_length=255, null=True)  # Adresse de livraison
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"
    
# Models pour les notifications de notre application
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification pour {self.user.username} : {self.message[:20]}..."