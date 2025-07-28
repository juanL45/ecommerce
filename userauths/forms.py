from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User,Profile

class UserRegisterForn(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Usuario"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Correo"}))
    password1 =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Contraseña"}))
    password2 =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirmacion"}))
    class Meta:
        model = User
        fields =['username','email']
        error_messages = {
                'username': {
                    'required': "Nombre de Usuario requerido"
                },
                'email': {
                    'unique': "Este correo ya existe",
                    'required': "Correo requerido"
                },
                 'password_mismatch': "Tus contraseñas no coiciden",
            }
class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))

    class Meta:
        model= Profile
        fields = ["full_name","image","bio","phone"]