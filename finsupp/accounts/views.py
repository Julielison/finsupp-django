from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conta criada com sucesso! Faça login para continuar.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível criar a conta. Verifique os dados informados.')
        return super().form_invalid(form)

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'E-mail ou senha incorretos. Tente novamente.')
        return super().form_invalid(form)

class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Você foi desconectado com sucesso.')
        return super().dispatch(request, *args, **kwargs)

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Se o e-mail informado estiver cadastrado, você receberá as instruções em breve.',
        )
        return super().form_valid(form)

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

    def form_valid(self, form):
        messages.success(self.request, 'Sua senha foi redefinida com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível redefinir a senha.')
        return super().form_invalid(form)

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
