from django import forms

from .models import User

class UserRegisterForm(forms.ModelForm):
     
    password1 = forms.CharField( 
        label='Contraseña',
        required=True, 
        max_length=32,
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresar una contraseña'})
    )

    password2 = forms.CharField(
        label='Repetir Contraseña',
        required=True,
        max_length=32, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'})
    )

    class Meta:
        model = User
        # muestra todos los campos del modelo
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
            'password1',
            'password2',
        )        
        