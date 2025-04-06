# views.py
from django.core.mail import send_mail
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.utils import timezone

from rest_framework.decorators import api_view, authentication_classes, renderer_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from proyecto_prevencion.models import Usuario, OrganismoPublico, ComunaPlan, TiposMedidas, Medida, Indicador
from .forms import OrganismoForm, ComunaForm, TiposMedidasForm, MedidaForm
from proyecto_prevencion.utils.decorators import require_permission

# --- Vistas de autenticación ---

class AdminLoginView(LoginView):
    template_name = 'admins/admin_login.html'
    
    def get_success_url(self):
        return reverse_lazy('admin_usuarios')

# --- Usuarios ---

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def usuarios_list(request):
    aprobados = Usuario.objects.filter(is_superuser=False, aprobado=True)
    pendientes = Usuario.objects.filter(is_superuser=False, aprobado=False)
    context = {
        'approved_users': aprobados,
        'pending_users': pendientes,
    }
    return Response(context, template_name='admins/usuarios_list.html')

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
def aprobar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    usuario.aprobado = True
    usuario.save()

    # Enviar correo de notificación
    try:
        send_mail(
            'Cuenta Aprobada',
            'Su cuenta ha sido aprobada y ya puede ingresar a la plataforma.',
            'grupo1@backend-python.com',
            [usuario.username],
            fail_silently=False,
        )
        print("Correo enviado")
    except Exception as e:
        print("Error al enviar el correo")

    messages.success(request, "Usuario aprobado correctamente.")
    return redirect(reverse_lazy('admin_usuarios'))

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
def desactivar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    usuario.aprobado = False
    usuario.save()
    messages.success(request, "Usuario desactivado correctamente.")
    return redirect(reverse_lazy('admin_usuarios'))

# ------ Vistas para OrganismoPublico ------

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def organismo_list(request):
    organismos = OrganismoPublico.objects.filter(activo=True)
    return Response({'organismos': organismos}, template_name='admins/organismo_list.html')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def organismo_create(request):
    if request.method == 'POST':
        form = OrganismoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Organismo agregado correctamente.")
                return redirect('organismo_list')
            except Exception as e:
                messages.error(request, "Error al agregar organismo, por favor vuelva a intentar.")
                return redirect('organismo_create')
    else:
        form = OrganismoForm()
    return Response({'form': form, 'titulo': 'Agregar Organismo'}, template_name='admins/organismo_form.html')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def organismo_update(request, pk):
    organismo = get_object_or_404(OrganismoPublico, pk=pk)
    if request.method == 'POST':
        form = OrganismoForm(request.POST, instance=organismo)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Organismo actualizado correctamente.")
                return redirect('organismo_list')
            except Exception as e:
                messages.error(request, "Error al actualizar organismo, por favor vuelva a intentar.")
                return redirect('organismo_update', pk=pk)
    else:
        form = OrganismoForm(instance=organismo)
    return Response({'form': form, 'titulo': 'Editar Organismo'}, template_name='admins/organismo_form.html')

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
def organismo_delete(request, pk):
    organismo = get_object_or_404(OrganismoPublico, pk=pk)
    try:
        organismo.delete()
        messages.success(request, "Organismo eliminado correctamente.")
    except IntegrityError:
        organismo.activo = False
        organismo.save()
        messages.warning(request, "El organismo está referenciado; se desactivó en su lugar.")
    return redirect('organismo_list')

# ------ Vistas para ComunaPlan ------

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def comuna_list(request):
    comunas = ComunaPlan.objects.filter(activo=True)
    return Response({'comunas': comunas}, template_name='admins/comuna_list.html')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def comuna_create(request):
    if request.method == 'POST':
        form = ComunaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Comuna agregada correctamente.")
                return redirect('comuna_list')
            except Exception as e:
                messages.error(request, "Error al agregar comuna, por favor vuelva a intentar.")
                return redirect('comuna_create')
    else:
        form = ComunaForm()
    return Response({'form': form, 'titulo': 'Agregar Comuna'}, template_name='admins/comuna_form.html')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def comuna_update(request, pk):
    comuna = get_object_or_404(ComunaPlan, pk=pk)
    if request.method == 'POST':
        form = ComunaForm(request.POST, instance=comuna)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Comuna actualizada correctamente.")
                return redirect('comuna_list')
            except Exception as e:
                messages.error(request, "Error al actualizar comuna, por favor vuelva a intentar.")
                return redirect('comuna_update', pk=pk)
    else:
        form = ComunaForm(instance=comuna)
    return Response({'form': form, 'titulo': 'Editar Comuna'}, template_name='admins/comuna_form.html')

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
def comuna_delete(request, pk):
    comuna = get_object_or_404(ComunaPlan, pk=pk)
    try:
        comuna.delete()
        messages.success(request, "Comuna eliminada correctamente.")
    except IntegrityError:
        comuna.activo = False
        comuna.save()
        messages.warning(request, "La comuna está referenciada; se desactivó en su lugar.")
    return redirect('comuna_list')

# ------ Vistas para TiposMedidas ------

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def tipomedida_list(request):
    medidas = TiposMedidas.objects.filter(activo=True)
    return Response({'medidas': medidas}, template_name='admins/tipomedida_list.html')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def tipomedida_create(request):
    if request.method == 'POST':
        form = TiposMedidasForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Tipo de medida agregado correctamente.")
                return redirect('tipomedida_list')
            except Exception as e:
                print(str(e))
                messages.error(request, "Error al agregar tipo de medida, por favor vuelva a intentar.")
                return redirect('tipomedida_create')
    else:
        form = TiposMedidasForm()
    return Response({'form': form, 'titulo': 'Agregar Tipo de Medida'}, template_name='admins/tipomedida_form.html')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def tipomedida_update(request, pk):
    medida = get_object_or_404(TiposMedidas, pk=pk)
    if request.method == 'POST':
        form = TiposMedidasForm(request.POST, instance=medida)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Tipo de medida actualizado correctamente.")
                return redirect('tipomedida_list')
            except Exception as e:
                messages.error(request, "Error al actualizar tipo de medida, por favor vuelva a intentar.")
                return redirect('tipomedida_update', pk=pk)
    else:
        form = TiposMedidasForm(instance=medida)
    return Response({'form': form, 'titulo': 'Editar Tipo de Medida'}, template_name='admins/tipomedida_form.html')

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
def tipomedida_delete(request, pk):
    medida = get_object_or_404(TiposMedidas, pk=pk)
    try:
        medida.delete()
        messages.success(request, "Tipo de medida eliminado correctamente.")
    except IntegrityError:
        medida.activo = False
        medida.save()
        messages.warning(request, "El tipo de medida está referenciado; se desactivó en su lugar.")
    return redirect('tipomedida_list')

# ------ Vistas para Medidas ------

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def medida_list(request):
    medidas = Medida.objects.filter(activo=True)
    return Response({'medidas': medidas}, template_name='admins/medida_list.html')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def medida_create(request):
    if request.method == 'POST':
        form = MedidaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Medida agregada correctamente.")
                return redirect('medida_list')
            except Exception as e:
                messages.error(request, "Error al agregar la medida, por favor vuelva a intentar.")
                return redirect('medida_create')
    else:
        form = MedidaForm()
    return Response({'form': form, 'titulo': 'Agregar Medida'}, template_name='admins/medida_form.html')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def medida_update(request, pk):
    medida = get_object_or_404(Medida, pk=pk)
    if request.method == 'POST':
        form = MedidaForm(request.POST, instance=medida)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Medida actualizada correctamente.")
                return redirect('medida_list')
            except Exception as e:
                messages.error(request, "Error al actualizar la medida, por favor vuelva a intentar.")
                return redirect('medida_update', pk=pk)
    else:
        form = MedidaForm(instance=medida)
    return Response({'form': form, 'titulo': 'Editar Medida'}, template_name='admins/medida_form.html')

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
def medida_delete(request, pk):
    medida = get_object_or_404(Medida, pk=pk)
    try:
        medida.delete()
        messages.success(request, "Medida eliminado correctamente.")
    except IntegrityError:
        medida.activo = False
        medida.save()
        messages.warning(request, "La medida está referenciado; se desactivó en su lugar.")
    return redirect('medida_list')

# ------ Vistas para Indicadores ------

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
@renderer_classes([TemplateHTMLRenderer])
def indicadores_list(request):
    indicadores = Indicador.objects.select_related('medida', 'usuario')\
        .prefetch_related('documentos_subidos')\
        .order_by('-fecha_reporte')
    
    return Response({'indicadores': indicadores}, template_name='admins/indicadores_list.html')

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
def aprobar_indicador(request, pk):
    indicador = get_object_or_404(Indicador, pk=pk)
    indicador.cumple_requisitos = True
    indicador.fecha_aprobacion = timezone.now()
    indicador.fecha_rechazo = None
    indicador.motivo_rechazo = ""
    indicador.save()

    medida = indicador.medida
    if medida.frecuencia == 'anual':
        medida.proxima_fecha_carga = timezone.now().date() + relativedelta(years=+1)
    elif medida.frecuencia == 'unica':
        medida.proxima_fecha_carga = None
    medida.save()

    messages.success(request, "Indicador aprobado correctamente.")
    return redirect('indicadores_list')

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@require_permission(lambda user: user.is_superuser, redirect_url='home', error_message="No cuenta con permisos para acceder a esta sección.")
def rechazar_indicador(request, pk):
    indicador = get_object_or_404(Indicador, pk=pk)
    
    motivo = request.POST.get('motivo', '').strip()
    if not motivo:
        messages.error(request, "Debe indicar un motivo de rechazo.")
        return redirect('indicadores_list')
    
    indicador.cumple_requisitos = False
    indicador.fecha_aprobacion = None
    indicador.fecha_rechazo = timezone.now()
    indicador.motivo_rechazo = motivo
    indicador.save()
    messages.warning(request, "Indicador rechazado correctamente.")
    return redirect('indicadores_list')