# usuarios/views.py
import os
import uuid
from django.core.files.storage import default_storage
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .forms import UsuarioRegistrationForm
from django.urls import reverse_lazy

# Importaciones de DRF
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from proyecto_prevencion.models import Medida, Indicador, DocumentoSubido
from .forms import generar_subir_documentos_form
from proyecto_prevencion.utils.decorators import require_permission


class UserLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def register(request):
    if request.method == 'POST':
        form = UsuarioRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registro exitoso. Se le avisará cuando su cuenta sea validada.")
            return redirect('home')
    else:
        form = UsuarioRegistrationForm()
    return render(request, 'usuarios/register.html', {'form': form})


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
@require_permission(lambda user: not user.is_superuser, redirect_url='home', error_message="Los administradores no pueden subir documentos.")
@renderer_classes([TemplateHTMLRenderer])
def dashboard(request):
    user = request.user
    measures = Medida.objects.filter(organismo=user.organismo, activo=True)

    approved = []
    pending_review = []
    rejected = []
    pending_completion = []

    for measure in measures:
        indicator = Indicador.objects.filter(
            medida=measure, usuario=user).order_by('-fecha_reporte').first()
        if indicator:
            if indicator.cumple_requisitos:
                approved.append((measure, indicator))
            else:
                if indicator.fecha_rechazo:
                    rejected.append((measure, indicator))
                else:
                    pending_review.append((measure, indicator))
        else:
            pending_completion.append(measure)

    context = {
        'approved': approved,
        'pending_review': pending_review,
        'rejected': rejected,
        'pending_completion': pending_completion,
    }
    return Response(context, template_name='usuarios/dashboard.html')


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
@require_permission(lambda user: not user.is_superuser, redirect_url='home', error_message="Los administradores no pueden subir documentos.")
@renderer_classes([TemplateHTMLRenderer])
def subir_documentos(request, medida_id):
    user = request.user
    medida = get_object_or_404(Medida, pk=medida_id)

    if medida.organismo != user.organismo:
        messages.error(
            request, "No tienes permiso para subir documentos para esta medida.")
        return redirect(reverse_lazy('usuario_dashboard'))

    documentos = medida.documentos_requeridos.all()
    SubirDocumentosForm = generar_subir_documentos_form(documentos)

    if request.method == 'POST':
        form = SubirDocumentosForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                indicador = Indicador.objects.create(
                    medida=medida,
                    usuario=user,
                    calculo_indicador=0,
                    cumple_requisitos=False
                )
                for doc in documentos:
                    field_name = f'doc_{doc.id}'
                    file = form.cleaned_data.get(field_name)
                    if file:
                        original_extension = os.path.splitext(file.name)[1]
                        unique_filename = f"{uuid.uuid4().hex}_doc_{doc.id}{original_extension}"
                        filename = default_storage.save(unique_filename, file)
                        DocumentoSubido.objects.create(
                            indicador=indicador,
                            documento_requerido=doc,
                            archivo=filename,
                        )
                messages.success(
                    request, "Documentos subidos correctamente. Espera validación del admin.")
                return redirect('usuario_dashboard')
            except Exception as e:
                error_text = str(e).splitlines()[0]
                messages.error(
                    request, "Error al subir documentos: " + error_text)
                return redirect('subir_documentos', medida_id=medida.id)
    else:
        form = SubirDocumentosForm()

    fields_list = []
    for doc in documentos:
        field_name = f"doc_{doc.id}"
        fields_list.append((doc.descripcion, form[field_name]))

    context = {
        'form': form,
        'medida': medida,
        'fields_list': fields_list,
        'documentos': documentos,
        'titulo': 'Subir Documentos para ' + medida.nombre_corto,
    }
    return Response(context, template_name='usuarios/subir_documentos.html')
