from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        help_text=''
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text=''
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput,
        help_text=''
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password is not None and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    password = None  # Elimina el campo password
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {'username': '', 'first_name': '',  'last_name': '', 'email': ''}