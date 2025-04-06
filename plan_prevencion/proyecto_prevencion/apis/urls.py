# admin/urls.py
from django.urls import path
from .views import organismos, comuna_plan, tipos_medida, medida, indicador, usuario, admins_usuarios

urlpatterns = [
    # Rutas para Admin - Usuarios
    path('admin/usuarios/', admins_usuarios.api_usuarios_list, name='api_admin_usuarios'),
    path('admin/aprobar/<int:user_id>/', admins_usuarios.api_aprobar_usuario, name='api_aprobar_usuario'),
    path('admin/desactivar/<int:user_id>/', admins_usuarios.api_desactivar_usuario, name='api_desactivar_usuario'),

    # Rutas para OrganismoPublico
    path('admin/organismos/', organismos.api_organismo_list, name='api_organismo_list'),
    path('admin/organismos/add/', organismos.api_organismo_create, name='api_organismo_create'),
    path('admin/organismos/edit/<int:pk>/', organismos.api_organismo_update, name='api_organismo_update'),
    path('admin/organismos/delete/<int:pk>/', organismos.api_organismo_delete, name='api_organismo_delete'),
    
    # Rutas para ComunaPlan
    path('admin/comunas/', comuna_plan.api_comuna_list, name='api_comuna_list'),
    path('admin/comunas/add/', comuna_plan.api_comuna_create, name='api_comuna_create'),
    path('admin/comunas/edit/<int:pk>/', comuna_plan.api_comuna_update, name='api_comuna_update'),
    path('admin/comunas/delete/<int:pk>/', comuna_plan.api_comuna_delete, name='api_comuna_delete'),

    # Rutas para TiposMedidas
    path('admin/tiposmedidas/', tipos_medida.api_tipomedida_list, name='api_tipomedida_list'),
    path('admin/tiposmedidas/add/', tipos_medida.api_tipomedida_create, name='api_tipomedida_create'),
    path('admin/tiposmedidas/edit/<int:pk>/', tipos_medida.api_tipomedida_update, name='api_tipomedida_update'),
    path('admin/tiposmedidas/delete/<int:pk>/', tipos_medida.api_tipomedida_delete, name='api_tipomedida_delete'),

    # Rutas para Medidas
    path('admin/medida/', medida.api_medida_list, name='api_medida_list'),
    path('admin/medida/add/', medida.api_medida_create, name='api_medida_create'),
    path('admin/medida/edit/<int:pk>/', medida.api_medida_update, name='api_medida_update'),
    path('admin/medida/delete/<int:pk>/', medida.api_medida_delete, name='api_medida_delete'),

    # Rutas para Indicadores
    path('admin/indicadores/', indicador.api_indicadores_list, name='api_indicadores_list'),
    path('admin/indicadores/aprobar/<int:pk>/', indicador.api_aprobar_indicador, name='api_aprobar_indicador'),
    path('admin/indicadores/rechazar/<int:pk>/', indicador.api_rechazar_indicador, name='api_rechazar_indicador'),

    # Usuarios
    path('usuario/register/', usuario.api_register, name='api_register'),
    path('usuario/dashboard/', usuario.api_dashboard, name='api_usuario_dashboard'),
    path('usuario/medidas/subir/<int:medida_id>/', usuario.api_subir_documentos, name='api_subir_documentos'),
    path('usuario/medidas/<int:medida_id>/documentos-requeridos/', usuario.listar_documentos_requeridos, name='api_documentos_requeridos'),
]
