from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from proyecto_prevencion.apis.permissions import IsSuperUser
from proyecto_prevencion.models import OrganismoPublico
from proyecto_prevencion.apis.serializers import OrganismoPublicoSerializer

@extend_schema(
    tags=["Organismos"],
    summary="Listar organismos",
    description=(
        "Devuelve una lista de todos los organismos públicos activos registrados en el sistema.\n\n"
        "Los organismos representan a entidades del Estado responsables de coordinar, ejecutar y reportar "
        "las medidas definidas en el Plan de Prevención y Descontaminación Atmosférica (PPDA) "
        "para las comunas de Concón, Quintero y Puchuncaví.\n\n"
        "Cada organismo tiene a su cargo medidas específicas, y es el responsable de cargar los documentos necesarios "
        "para que la Superintendencia del Medio Ambiente pueda verificar el cumplimiento del plan."
    ),
    responses=OrganismoPublicoSerializer(many=True)
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_organismo_list(request):
    try:
        organismos = OrganismoPublico.objects.filter(activo=True)
        serializer = OrganismoPublicoSerializer(organismos, many=True)
        return Response({"success": True, "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)

@extend_schema(
    tags=["Organismos"],
    summary="Crear organismo",
    description=(
        "Registra un nuevo organismo público en el sistema para que pueda ser asignado a medidas dentro del PPDA.\n\n"
        "Una vez creado, este organismo podrá ser vinculado a usuarios y medidas, "
        "permitiendo el seguimiento de sus responsabilidades y la carga de documentos asociados al cumplimiento ambiental."
    ),
    request=OrganismoPublicoSerializer,
    responses=OrganismoPublicoSerializer
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_organismo_create(request):
    try:
        serializer = OrganismoPublicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=200)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)

@extend_schema(
    tags=["Organismos"],
    summary="Actualizar organismo",
    description=(
        "Permite actualizar la información de un organismo público ya registrado, de forma parcial o completa.\n\n"
        "Es útil para mantener actualizados los datos de la institución responsable de medidas en el marco del PPDA."
    ),
    request=OrganismoPublicoSerializer,
    responses=OrganismoPublicoSerializer
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_organismo_update(request, pk):
    try:
        organismo = get_object_or_404(OrganismoPublico, pk=pk)
        serializer = OrganismoPublicoSerializer(organismo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=200)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)

@extend_schema(
    tags=["Organismos"],
    summary="Eliminar organismo",
    description=(
        "Elimina un organismo público del sistema.\n\n"
        "Si el organismo está vinculado a medidas u otras entidades, no podrá eliminarse directamente y se deberá "
        "desactivar o revisar sus relaciones previamente.\n\n"
        "Esto asegura la integridad de los datos históricos del PPDA y su trazabilidad ante fiscalizaciones."
    ),
    responses={"success": bool, "message": str}
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_organismo_delete(request, pk):
    try:
        organismo = get_object_or_404(OrganismoPublico, pk=pk)
        organismo.delete()
        return Response({"success": True, "message": "Organismo eliminado correctamente."}, status=200)
    except IntegrityError as e:
        return Response({"success": False, "error": "No se puede eliminar el organismo porque está siendo utilizado."}, status=409)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
