from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from django.views.generic import (
    View,
    CreateView
)

from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UpdatePasswordForm
)

from .models import User

from .functions import code_generator


# Create your views here.
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):

        # generamos el codigo
        codigo = code_generator()

        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            # extra_fields
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codigo_registro=codigo
        )
        # enviar email al usuario
        asunto = 'Confirmación de email'
        mensaje = 'Codigo de verificación: ' + codigo
        email_remitente  = 'cris.vidal04@gmail.com'
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        # rederigir a pantalla de validacion
        # return super(UserRegisterView, self).form_valid(form)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )
            

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user # usuario en sesion
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password_actual'],
        )

        if user: # validar datos del usuario
            new_password = form.cleaned_data['password_nueva']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request) # cerrar sesion
        return super(UpdatePasswordView, self).form_valid(form)