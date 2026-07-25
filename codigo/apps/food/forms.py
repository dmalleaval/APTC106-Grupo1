from django import forms
from .models import Producto


class FoodsForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
