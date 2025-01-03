from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from store.forms import DeliveryPersonForm, ReviewForm, SignUpForm, UserUpdateForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal  # Assurez-vous d'importer Decimal

from .models import Cart, CartItem, DeliveryPerson, Notification, Order, OrderItem, Product, Review, User

from django.shortcuts import render



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte l'utilisateur après l'inscription
            return redirect('home')  # Redirige vers la page d'accueil (ou une autre page)
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    logout(request)  # Déconnecte l'utilisateur
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')  # Redirige vers la page de connexion

def custom_signup(request):
    if request.method == 'POST':
        # Créer une instance de UserCreationForm avec les données envoyées par le formulaire
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'registration/signup.html')

        try:
            # Créer l'utilisateur
            user = User.objects.create_user(username=username, password=password)
            # Connexion immédiate après inscription
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil ou la page désirée
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")
            return render(request, 'registration/signup.html')
    else:
        return render(request, 'registration/signup.html')

@login_required
def profile(request):
    return render(request, 'store/profile.html')
def home(request):
    # je veux envoyer l'utilisateur connecter en context a ma vue
    user = request.user
    return render(request, 'store/home.html', {'user': user})

def product_list(request):
    # Récupérer tous les produits
    products = Product.objects.all()
    product = Product.objects.get(name='Produit 3')
    print(product.image)
    
    return render(request, 'store/product_list.html', {'products': products})

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    #je veux passer en context le nom du livreur assigner a la livraison de cette commande si jamais il y a 
    
    return render(request, 'store/cart.html', {'cart': cart})

# Vue pour ajouter un produit au panier
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Appliquer la réduction sur le produit si elle existe
    final_price = product.price_with_discount() if product.discount else product.price
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    

    # Vérifie si le produit est déjà dans le panier
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:  # Si l'article existe déjà, on augmente la quantité
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

# Vue pour supprimer un produit du panier
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

# Vue pour mettre à jour la quantité d’un produit
@login_required
def update_quantity(request, cart_item_id):
    quantity = request.POST.get('quantity', 1)  # Get quantity from POST data, default to 1
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if quantity.isdigit() and int(quantity) > 0:  # Check if quantity is a positive integer
        cart_item.quantity = int(quantity)
        cart_item.save()
    return redirect('view_cart')
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        messages.error(request, "Votre panier est vide.")
        return redirect('view_cart')

    total_price = sum(item.product.price_with_discount() * item.quantity for item in cart_items)
    delivery_fee = Decimal('5.00')  # Convertir le prix de livraison en Decimal

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=total_price + delivery_fee, delivery_fee=delivery_fee)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price_with_discount()
            )
        cart.items.all().delete()

        # Créer une notification pour l'utilisateur
        Notification.objects.create(
            user=request.user,
            message=f"Votre commande #{order.id} a été validée avec succès !"
        )

        messages.success(request, f"Votre commande #{order.id} a été validée avec succès !")
        return redirect('order_history')

    return render(request, 'store/checkout.html', {'cart': cart, 'total_price': total_price, 'delivery_fee': delivery_fee})

# Vue pour ajouter un produit aux favoris
@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.favorites.add(product)
    return redirect('view_favorites')  # Rediriger vers le panier ou une page de favoris

# Vue pour afficher les favoris
@login_required
def view_favorites(request):
    return render(request, 'store/favorites.html', {'favorites': request.user.favorites.all()})

# Vue pour supprimer un produit des favoris
@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.favorites.remove(product)  # Supprime le produit des favoris
    messages.success(request, f"{product.name} a été supprimé de vos favoris.")
    return redirect('view_favorites')  # Redirige vers la page des favoris
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'store/add_review.html', {'form': form, 'product': product})

# Vue pour afficher un produit avec ses avis
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
            # Effectuer le processus d'achat immédiat ici (par exemple, rediriger vers la page de paiement)
        return HttpResponseRedirect(reverse('checkout'))  # Redirigez l'utilisateur vers la page de paiement
    reviews = product.reviews.all()  # Récupère tous les avis pour ce produit
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews})

# Vue pour ajouter un avis
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            return redirect('product_detail', product_id=product.id)
    return render(request, 'store/add_review.html', {'product': product})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/notifications.html', {'notifications': user_notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')   

def delivery_person_list(request):
    delivery_people = DeliveryPerson.objects.all()
    return render(request, 'store/delivery_person_list.html', {'delivery_people': delivery_people})

def add_delivery_person(request):
    if request.method == 'POST':
        form = DeliveryPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('delivery_person_list')
    else:
        form = DeliveryPersonForm()
    return render(request, 'store/add_delivery_person.html', {'form': form})

def update_delivery_person(request, pk):
    delivery_person = get_object_or_404(DeliveryPerson, pk=pk)
    if request.method == 'POST':
        form = DeliveryPersonForm(request.POST, instance=delivery_person)
        if form.is_valid():
            form.save()
            return redirect('delivery_person_list')
    else:
        form = DeliveryPersonForm(instance=delivery_person)
    return render(request, 'store/update_delivery_person.html', {'form': form})

def assign_delivery_person(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    delivery_people = DeliveryPerson.objects.filter(is_available=True)
    if request.method == 'POST':
        delivery_person_id = request.POST.get('delivery_person')
        delivery_person = get_object_or_404(DeliveryPerson, id=delivery_person_id)
        
        # Récupérer l'adresse de livraison depuis le formulaire
        delivery_address = request.POST.get('delivery_address')
        
        order.delivery_person = delivery_person
        order.status = 'in_progress'
        order.delivery_address = delivery_address  # Assigner l'adresse de livraison à la commande
        order.save()

        # Assigner le livreur au panier
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.delivery_person = delivery_person  # Assigner le livreur au panier
        cart.save()  # Sauvegarder le panier

        delivery_person.is_available = False  # Marquer le livreur comme indisponible
        delivery_person.save()

        # Créer une notification pour le livreur
        Notification.objects.create(
            user=delivery_person.user,
            message=f"Vous avez été assigné à la commande #{order.id}."
        )

        return redirect('view_cart')
    return render(request, 'store/assign_delivery_person.html', {'order': order, 'delivery_people': delivery_people})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'store/profile_update.html'  # Créez ce template pour le formulaire
    success_url = reverse_lazy('profile')  # Redirige après la mise à jour

    def get_object(self):
        return self.request.user  # Met à jour l'utilisateur connecté

@login_required
def delivery_dashboard(request):
    # Récupérer les missions de livraison assignées à l'utilisateur
    delivery_person = get_object_or_404(DeliveryPerson, user=request.user)
    missions = Order.objects.filter(delivery_person=delivery_person, status='in_progress')
    
    # Calculer les gains du livreur
    total_earnings = sum(order.delivery_fee for order in Order.objects.filter(delivery_person=delivery_person))

    return render(request, 'store/delivery_dashboard.html', {'missions': missions, 'total_earnings': total_earnings})
