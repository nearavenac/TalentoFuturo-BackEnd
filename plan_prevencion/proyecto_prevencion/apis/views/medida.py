from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from proyecto_prevencion.apis.permissions import IsSuperUser
from proyecto_prevencion.models import Medida
from proyecto_prevencion.serializers import MedidaSerializer

@extend_schema(
    tags=["Medidas"],
    summary="Listar medidas",
    description=(
        "Devuelve una lista de todas las medidas activas registradas en el sistema.\n\n"
        "Las medidas representan las acciones comprometidas dentro del Plan de Prevención y Descontaminación Atmosférica (PPDA) "
        "para las comunas de Concón, Quintero y Puchuncaví.\n\n"
        "Cada medida está vinculada a un organismo público responsable, tiene una frecuencia de reporte y puede requerir el envío "
        "de documentos que permitan verificar su cumplimiento por parte de la Superintendencia del Medio Ambiente."
    ),
    responses=MedidaSerializer(many=True)
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_medida_list(request):
    try:
        medidas = Medida.objects.filter(activo=True)
        serializer = MedidaSerializer(medidas, many=True)
        return Response({"success": True, "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Medidas"],
    summary="Crear medida",
    description=(
        "Crea una nueva medida dentro del sistema.\n\n"
        "Estas medidas corresponden a acciones que deben ser implementadas por organismos públicos, y están alineadas "
        "con los objetivos del PPDA. Cada medida puede ser regulatoria o no, tener una frecuencia de cumplimiento específica "
        "y requerir el envío de documentación.\n\n"
        "🔧 **Requiere enviar en el body (JSON):**\n"
        "- `tipo_medida` (ID): Tipo de medida (consultar [Tipos de Medidas](/api/docs#/Tipos%20de%20Medidas))\n"
        "- `organismo` (ID): Organismo responsable (ver [Organismos](/api/docs#/Organismos))\n"
        "- `nombre_corto`, `nombre_largo`, `descripcion_formula`, `tipo_formula`, `frecuencia`, etc.\n\n"
        "📌 Los campos `tipo_formula` y `frecuencia` tienen valores predefinidos (choices)."
    ),
    request=MedidaSerializer,
    responses=MedidaSerializer
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_medida_create(request):
    try:
        serializer = MedidaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=200)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Medidas"],
    summary="Actualizar medida",
    description=(
        "Permite modificar parcial o totalmente los datos de una medida ya existente.\n\n"
        "Esto puede utilizarse para corregir datos, cambiar la frecuencia de cumplimiento o reasignar el organismo responsable, "
        "siempre dentro del marco de seguimiento del PPDA."
    ),
    request=MedidaSerializer,
    responses=MedidaSerializer
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_medida_update(request, pk):
    try:
        medida = get_object_or_404(Medida, pk=pk)
        serializer = MedidaSerializer(medida, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=200)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Medidas"],
    summary="Eliminar medida",
    description=(
        "Elimina una medida registrada por su ID.\n\n"
        "Si la medida está relacionada con indicadores, documentos u otros elementos del sistema, no se elimina directamente, "
        "sino que se marca como inactiva para conservar el historial y mantener la trazabilidad del cumplimiento del PPDA."
    ),
    responses={"success": bool, "message": str}
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_medida_delete(request, pk):
    try:
        medida = get_object_or_404(Medida, pk=pk)
        medida.delete()
        return Response({"success": True, "message": "Medida eliminada correctamente."}, status=200)
    except IntegrityError:
        medida.activo = False
        medida.save()
        return Response({"success": False, "message": "La medida está referenciada; se desactivó en su lugar."}, status=409)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
