from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from proyecto_prevencion.apis.permissions import IsSuperUser
from proyecto_prevencion.models import ComunaPlan
from proyecto_prevencion.apis.serializers import ComunaPlanSerializer

@extend_schema(
    tags=["Comunas"],
    summary="Listar comunas",
    description=(
        "Devuelve una lista de comunas activas que participan en el Plan de Prevención y Descontaminación Atmosférica (PPDA) "
        "para Concón, Quintero y Puchuncaví.\n\n"
        "Estas comunas forman parte de una estrategia impulsada por el Ministerio del Medio Ambiente y supervisada por la "
        "Superintendencia del Medio Ambiente (SMA), cuyo objetivo es mejorar la calidad del aire en la zona.\n\n"
        "El registro y seguimiento de las medidas que se implementan en estas comunas permite monitorear el avance del plan, "
        "verificar el cumplimiento de responsabilidades y facilitar la evaluación de resultados ambientales."
    ),
    responses=ComunaPlanSerializer(many=True)
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_comuna_list(request):
    try:
        comunas = ComunaPlan.objects.filter(activo=True)
        serializer = ComunaPlanSerializer(comunas, many=True)
        return Response({"success": True, "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Comunas"],
    summary="Crear comuna",
    description=(
        "Permite agregar una nueva comuna al sistema para incluirla en el monitoreo del Plan de Prevención y Descontaminación Atmosférica (PPDA).\n\n"
        "Las comunas incorporadas podrán ser asociadas a medidas específicas dentro del plan, lo que habilita su seguimiento y "
        "el registro de información ambiental relacionada a su avance."
    ),
    request=ComunaPlanSerializer,
    responses=ComunaPlanSerializer
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_comuna_create(request):
    try:
        serializer = ComunaPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=200)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Comunas"],
    summary="Actualizar comuna",
    description=(
        "Actualiza la información de una comuna registrada en el sistema.\n\n"
        "Esto permite corregir o completar datos relevantes de una comuna que participa en el PPDA, asegurando que toda "
        "la información necesaria para su seguimiento esté actualizada."
    ),
    request=ComunaPlanSerializer,
    responses=ComunaPlanSerializer
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_comuna_update(request, pk):
    try:
        comuna = get_object_or_404(ComunaPlan, pk=pk)
        serializer = ComunaPlanSerializer(comuna, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=200)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Comunas"],
    summary="Eliminar comuna",
    description=(
        "Elimina una comuna del sistema. Si la comuna tiene medidas u otros elementos relacionados, se desactiva en lugar de eliminarse definitivamente.\n\n"
        "Esta acción es útil cuando una comuna deja de participar activamente en el PPDA o necesita ser reemplazada por otra entidad."
    ),
    responses={"success": bool, "message": str}
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_comuna_delete(request, pk):
    try:
        comuna = get_object_or_404(ComunaPlan, pk=pk)
        comuna.delete()
        return Response({"success": True, "message": "Comuna eliminada correctamente."}, status=200)
    except IntegrityError:
        comuna.activo = False
        comuna.save()
        return Response({"success": False, "message": "La comuna está referenciada; se desactivó en su lugar."}, status=409)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
