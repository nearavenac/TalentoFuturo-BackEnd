# admin/urls.py
from django.urls import path
from .views import AdminLoginView
from . import views

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('usuarios/', views.usuarios_list, name='admin_usuarios'),
    path('aprobar/<int:user_id>/', views.aprobar_usuario, name='aprobar_usuario'),
    path('desactivar/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),

    # Rutas para OrganismoPublico
    path('organismos/', views.organismo_list, name='organismo_list'),
    path('organismos/add/', views.organismo_create, name='organismo_create'),
    path('organismos/edit/<int:pk>/', views.organismo_update, name='organismo_update'),
    path('organismos/delete/<int:pk>/', views.organismo_delete, name='organismo_delete'),

    # Rutas para ComunaPlan
    path('comunas/', views.comuna_list, name='comuna_list'),
    path('comunas/add/', views.comuna_create, name='comuna_create'),
    path('comunas/edit/<int:pk>/', views.comuna_update, name='comuna_update'),
    path('comunas/delete/<int:pk>/', views.comuna_delete, name='comuna_delete'),

    # Rutas para TiposMedidas
    path('tiposmedidas/', views.tipomedida_list, name='tipomedida_list'),
    path('tiposmedidas/add/', views.tipomedida_create, name='tipomedida_create'),
    path('tiposmedidas/edit/<int:pk>/', views.tipomedida_update, name='tipomedida_update'),
    path('tiposmedidas/delete/<int:pk>/', views.tipomedida_delete, name='tipomedida_delete'),

    # Rutas para Medidas
    path('medida/', views.medida_list, name='medida_list'),
    path('medida/add/', views.medida_create, name='medida_create'),
    path('medida/edit/<int:pk>/', views.medida_update, name='medida_update'),
    path('medida/delete/<int:pk>/', views.medida_delete, name='medida_delete'),

    # Rutas para Indicadores
    path('indicadores/', views.indicadores_list, name='indicadores_list'),
    path('indicadores/aprobar/<int:pk>/', views.aprobar_indicador, name='aprobar_indicador'),
    path('indicadores/rechazar/<int:pk>/', views.rechazar_indicador, name='rechazar_indicador'),
]
