from django import forms
from .models import Categoria, Producto


class FoodsForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
