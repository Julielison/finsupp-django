from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('cadastrar/', views.SignUpView.as_view(), name='signup'),
    path('entrar/', views.CustomLoginView.as_view(), name='login'),
    path('sair/', views.CustomLogoutView.as_view(), name='logout'),
    path('recuperar-senha/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('recuperar-senha/sucesso/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar-senha/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar-senha/concluida/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
