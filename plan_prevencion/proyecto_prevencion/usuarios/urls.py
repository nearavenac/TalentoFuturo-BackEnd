# usuarios/urls.py

from django.urls import path
from .views import UserLoginView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('dashboard/', views.dashboard, name='usuario_dashboard'),
    path('medidas/subir/<int:medida_id>/', views.subir_documentos, name='subir_documentos'),
]
