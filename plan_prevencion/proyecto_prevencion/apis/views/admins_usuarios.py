from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from proyecto_prevencion.models import Usuario
from proyecto_prevencion.apis.serializers import UsuarioSerializer
from proyecto_prevencion.apis.permissions import IsSuperUser


@extend_schema(
    tags=["Admin - Usuarios"],
    summary="Listar usuarios",
    description=(
        "Devuelve la lista de usuarios que pertenecen a los distintos organismos encargados de reportar medidas. "
        "Los usuarios están separados en dos grupos:\n\n"
        "- **Aprobados**: tienen acceso al sistema y pueden subir documentos requeridos para las medidas.\n"
        "- **Pendientes**: están registrados pero aún no han sido validados por el administrador.\n\n"
        "Cada usuario está vinculado a un organismo, y su función es subir información y documentación que será validada por el ente fiscalizador "
        "para corroborar el cumplimiento de las medidas establecidas."
    ),
    responses={
        200: OpenApiTypes.OBJECT,
        500: OpenApiTypes.OBJECT
    },
    examples=[
        OpenApiExample(
            name="Lista de usuarios",
            value={
                "success": True,
                "data": {
                    "approved_users": [
                        {"id": 1, "email": "usuario1@org.com", "aprobado": True}
                    ],
                    "pending_users": [
                        {"id": 2, "email": "usuario2@org.com", "aprobado": False}
                    ]
                }
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Error del servidor",
            value={
                "success": False,
                "error": "Error interno al listar usuarios."
            },
            response_only=True,
            status_codes=["500"]
        )
    ]
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_usuarios_list(request):
    try:
        aprobados = Usuario.objects.filter(is_superuser=False, aprobado=True)
        pendientes = Usuario.objects.filter(is_superuser=False, aprobado=False)

        return Response({
            "success": True,
            "data": {
                "approved_users": UsuarioSerializer(aprobados, many=True).data,
                "pending_users": UsuarioSerializer(pendientes, many=True).data
            }
        })
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Admin - Usuarios"],
    summary="Aprobar usuario",
    description=(
        "Aprueba un usuario registrado y lo habilita para ingresar al sistema.\n\n"
        "Una vez aprobado, el usuario podrá:\n"
        "- Acceder a su panel de carga\n"
        "- Visualizar las medidas asociadas a su organismo\n"
        "- Subir los documentos requeridos\n\n"
        "También se envía automáticamente un correo notificando al usuario que su cuenta ha sido habilitada."
    ),
    responses={
        200: OpenApiTypes.OBJECT,
        500: OpenApiTypes.OBJECT
    },
    examples=[
        OpenApiExample(
            name="Usuario aprobado",
            value={
                "success": True,
                "message": "Usuario aprobado correctamente."
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Aprobado pero falló el correo",
            value={
                "success": False,
                "message": "Usuario aprobado, pero falló el envío de correo."
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Error del servidor",
            value={
                "success": False,
                "error": "No se pudo aprobar el usuario."
            },
            response_only=True,
            status_codes=["500"]
        )
    ]
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_aprobar_usuario(request, user_id):
    try:
        usuario = get_object_or_404(Usuario, pk=user_id)
        usuario.aprobado = True
        usuario.save()

        try:
            send_mail(
                'Cuenta Aprobada',
                'Su cuenta ha sido aprobada y ya puede ingresar a la plataforma.',
                'grupo1@backend-python.com',
                [usuario.email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"success": False, "message": "Usuario aprobado, pero falló el envío de correo."}, status=200)

        return Response({"success": True, "message": "Usuario aprobado correctamente."}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


@extend_schema(
    tags=["Admin - Usuarios"],
    summary="Desactivar usuario",
    description=(
        "Desactiva un usuario previamente aprobado, impidiéndole el acceso al sistema.\n\n"
        "Esto puede utilizarse si el usuario cambia de función, si su organismo ya no participa en el programa, "
        "o si comete alguna infracción. Una vez desactivado:\n"
        "- El usuario no podrá acceder a su cuenta\n"
        "- No podrá cargar documentos ni reportar nuevas medidas\n"
        "- Su información permanece registrada, pero en estado inactivo"
    ),
    responses={
        200: OpenApiTypes.OBJECT,
        500: OpenApiTypes.OBJECT
    },
    examples=[
        OpenApiExample(
            name="Usuario desactivado",
            value={
                "success": True,
                "message": "Usuario desactivado correctamente."
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Error del servidor",
            value={
                "success": False,
                "error": "No se pudo desactivar el usuario."
            },
            response_only=True,
            status_codes=["500"]
        )
    ]
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def api_desactivar_usuario(request, user_id):
    try:
        usuario = get_object_or_404(Usuario, pk=user_id)
        usuario.aprobado = False
        usuario.save()
        return Response({"success": True, "message": "Usuario desactivado correctamente."}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
