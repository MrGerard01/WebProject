from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from web.models import Review


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=254, required=True)

    class Meta:
        model = User  # Usa el modelo User para la autenticación
        fields = ['username', 'email', 'password1', 'password2']  # No incluyas '<PASSWORD>'
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Email de Usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmación de Contraseña',
        }

class AuthenticationForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Usuario o contraseña incorrectos')
        return self.cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['titulo', 'rating', 'descripcion']