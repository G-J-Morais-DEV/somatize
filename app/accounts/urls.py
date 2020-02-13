from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, dashboard, edit, edit_password, password_reset, password_reset_confirm
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('entrar', LoginView.as_view(
        template_name='accounts/login.html'), name='login'),
    path('registrar', register, name='register'),
    path('nova_senha', password_reset, name='password_reset'),
    path('editar', edit, name='edit'),
    path('editar-senha', edit_password, name='edit_password'),
    path('confirmar_senha/<str:str>', password_reset_confirm,
         name='password_reset_confirm'),
    path('sair', LogoutView.as_view(next_page='home'), name='logout'),
]
