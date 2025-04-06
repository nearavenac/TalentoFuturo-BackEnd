from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from proyecto_prevencion.models import Indicador, Medida
from proyecto_prevencion.apis.serializers import IndicadorSerializer, RechazoIndicadorSerializer
from proyecto_prevencion.apis.permissions import IsSuperUser

@extend_schema(
    tags=["Indicadores"],
    summary="Listar indicadores",
        description=(
        "Devuelve todos los indicadores registrados en el sistema por el usuario autenticado, ordenados por fecha de reporte (más reciente primero).\n\n"
        "Un indicador representa una carga realizada por un usuario respecto al cumplimiento de una medida específica. "
        "Incluye el cálculo del indicador, el estado de validación (`cumple_requisitos`), y los documentos subidos como respaldo.\n\n"
        "Esta vista permite al administrador revisar el historial completo de indicadores para todas las medidas reportadas."
    ),
    responses=IndicadorSerializer(many=True)
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_indicadores_list(request):
    try:
        indicadores = Indicador.objects.select_related('medida', 'usuario')\
            .prefetch_related('documentos_subidos')\
            .order_by('-fecha_reporte')

        serializer = IndicadorSerializer(indicadores, many=True)
        return Response({"success": True, "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Indicadores"],
    summary="Aprobar indicador",
    description=(
        "Aprueba un indicador por su ID, marcando que cumple con los requisitos establecidos para la medida asociada.\n\n"
        "Además, actualiza automáticamente el campo `proxima_fecha_carga` de la medida según su frecuencia:\n"
        "- Si es anual: se calcula el siguiente año\n"
        "- Si es única: se deja sin nueva fecha\n\n"
        "Esto permite mantener actualizado el calendario de cumplimiento y seguimiento del PPDA."
    ),
    responses={"success": bool, "message": str}
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_aprobar_indicador(request, pk):
    try:
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

        return Response({"success": True, "message": "Indicador aprobado correctamente."}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Indicadores"],
    summary="Rechazar indicador",
    description=(
        "Rechaza un indicador por su ID. Se debe enviar en el body:\n\n"
        "{ \"motivo\": \"Falta documento firmado por la autoridad\" }\n\n"
        "Esto marcará el indicador como no válido, guardará la fecha de rechazo y registrará el motivo."
    ),
    request=RechazoIndicadorSerializer,
    responses={"success": bool, "message": str}
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_rechazar_indicador(request, pk):
    try:
        motivo = request.data.get('motivo', '').strip()
        if not motivo:
            return Response({"success": False, "error": "Debe indicar un motivo de rechazo."}, status=400)

        indicador = get_object_or_404(Indicador, pk=pk)
        indicador.cumple_requisitos = False
        indicador.fecha_aprobacion = None
        indicador.fecha_rechazo = timezone.now()
        indicador.motivo_rechazo = motivo
        indicador.save()

        return Response({"success": True, "message": "Indicador rechazado correctamente."}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
