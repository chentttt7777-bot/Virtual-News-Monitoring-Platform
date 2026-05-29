from django.urls import path
from . import views
from .views import (
     login_view, register_view, logout_view,
    clear_login_error, clear_register_error,save_history, get_history,clear_history
)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clear-login-error/', clear_login_error, name='clear_login_error'),
    path('clear-register-error/', clear_register_error, name='clear_register_error'),
    path('save-history/', save_history, name='save_history'),
    path('get-history/', get_history, name='get_history'),
    path('clear-history/', clear_history, name='clear_history'),
]
