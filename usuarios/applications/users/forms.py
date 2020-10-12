from django import forms

from .models import User

class UserRegisterForm(forms.ModelForm):

    class Meta:
        model = User
        # muestra todos los campos del modelo
        fields = ('__all__')        
        