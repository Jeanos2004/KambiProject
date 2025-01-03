from django import forms
from .models import DeliveryPerson, Review, User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
class DeliveryPersonForm(forms.ModelForm):
    class Meta:
        model = DeliveryPerson
        fields = ['user', 'phone_number', 'address', 'is_available']
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture']