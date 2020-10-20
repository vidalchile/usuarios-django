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
        # muestra solo algunos campos del modelo
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
            'password1',
            'password2',
        )
    
    def clean_password2(self):
        if len(self.cleaned_data['password1']) < 5:
            self.add_error('password1', 'Las contraseña debe tener mas de 5 digitos')
        elif self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
     
    username = forms.CharField( 
        label='username',
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    password = forms.CharField( 
        label='Contraseña',
        required=True, 
        max_length=32,
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresar contraseña'})
    )
        