from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from proyecto_prevencion.apis.permissions import IsSuperUser
from proyecto_prevencion.models import TiposMedidas
from proyecto_prevencion.apis.serializers import TiposMedidasSerializer

@extend_schema(
    tags=["Tipos de Medidas"],
    summary="Listar tipos de medidas",
    description=(
        "Devuelve una lista de todos los tipos de medidas activas disponibles en el sistema.\n\n"
        "Estos tipos corresponden a categorías generales utilizadas para clasificar medidas **no regulatorias** dentro del Plan de Prevención "
        "y Descontaminación Atmosférica (PPDA).\n\n"
        "Ejemplos comunes de tipos de medidas son:\n"
        "- Política Pública\n"
        "- Educación y difusión\n"
        "- Estudios\n\n"
        "Esta clasificación facilita la organización de las acciones según su naturaleza y propósito."
    ),
    responses=TiposMedidasSerializer(many=True)
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_tipomedida_list(request):
    try:
        medidas = TiposMedidas.objects.filter(activo=True)
        serializer = TiposMedidasSerializer(medidas, many=True)
        return Response({"success": True, "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Tipos de Medidas"],
    summary="Crear tipo de medida",
    description=(
        "Registra un nuevo tipo de medida para ser utilizado en la clasificación de medidas no regulatorias del PPDA.\n\n"
        "Estos tipos permiten distinguir el enfoque de cada acción (por ejemplo: campañas educativas, estudios técnicos, etc.) "
        "y mejorar el seguimiento del plan según su naturaleza."
    ),
    request=TiposMedidasSerializer,
    responses=TiposMedidasSerializer
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_tipomedida_create(request):
    try:
        serializer = TiposMedidasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=200)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Tipos de Medidas"],
    summary="Actualizar tipo de medida",
    description=(
        "Permite modificar los datos de un tipo de medida existente, identificado por su ID.\n\n"
        "Se utiliza para corregir nombres o actualizar categorías asociadas a medidas no regulatorias del PPDA."
    ),
    request=TiposMedidasSerializer,
    responses=TiposMedidasSerializer
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_tipomedida_update(request, pk):
    try:
        medida = get_object_or_404(TiposMedidas, pk=pk)
        serializer = TiposMedidasSerializer(medida, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=200)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Tipos de Medidas"],
    summary="Eliminar tipo de medida",
    description=(
        "Elimina un tipo de medida del sistema. Si el tipo está en uso por medidas existentes, se desactiva automáticamente para conservar la integridad de los datos.\n\n"
        "Esto permite mantener el historial de uso sin afectar registros anteriores."
    ),
    responses={"success": bool, "message": str}
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_tipomedida_delete(request, pk):
    try:
        medida = get_object_or_404(TiposMedidas, pk=pk)
        medida.delete()
        return Response({"success": True, "message": "Tipo de medida eliminado correctamente."}, status=200)
    except IntegrityError:
        medida.activo = False
        medida.save()
        return Response({"success": False, "message": "El tipo de medida está referenciado; se desactivó en su lugar."}, status=409)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
