from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from proyecto_prevencion.apis.permissions import IsRegularApprovedUser
from proyecto_prevencion.models import Medida, Indicador, DocumentoSubido
from proyecto_prevencion.serializers import UsuarioRegistrationSerializer, MedidaSerializer, DashboardResponseSerializer, generar_documentos_serializer

@extend_schema(
    tags=["Usuarios"],
    summary="Registro de usuario",
    description="Registra un nuevo usuario. La cuenta quedará pendiente de validación por un administrador.",
    request=UsuarioRegistrationSerializer,
    responses={"success": bool, "message": str}
)
@api_view(['POST'])
def api_register(request):
    serializer = UsuarioRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Registro exitoso. Se le avisará cuando su cuenta sea validada."
        }, status=200)
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)


@extend_schema(
    tags=["Usuarios"],
    summary="Dashboard del usuario",
    description=(
        "Devuelve la información del usuario autenticado respecto a sus medidas activas, "
        "su estado en relación con los indicadores más recientes, y los documentos requeridos por cada medida.\n\n"
        "Categorías de resultados:\n"
        "- `approved`: Medidas con indicadores aprobados.\n"
        "- `pending_review`: Indicadores enviados pero aún no revisados.\n"
        "- `rejected`: Indicadores rechazados con motivo.\n"
        "- `pending_completion`: Medidas sin ningún indicador enviado aún.\n\n"
        "Cada medida incluye los documentos requeridos en el campo `documentos_requeridos`, con `id` y `descripcion`."
    ),
    responses=DashboardResponseSerializer
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsRegularApprovedUser])
def api_dashboard(request):
    user = request.user
    measures = Medida.objects.filter(organismo=user.organismo, activo=True).prefetch_related("documentos_requeridos")

    approved = []
    pending_review = []
    rejected = []
    pending_completion = []

    for measure in measures:
        indicador = Indicador.objects.filter(
            medida=measure, usuario=user).order_by('-fecha_reporte').first()

        medida_serializada = MedidaSerializer(measure).data

        if indicador:
            item = {
                "medida": medida_serializada,
                "indicador_id": indicador.id,
                "cumple_requisitos": indicador.cumple_requisitos,
                "fecha_reporte": indicador.fecha_reporte
            }

            if indicador.cumple_requisitos:
                approved.append(item)
            elif indicador.fecha_rechazo:
                rejected.append(item)
            else:
                pending_review.append(item)
        else:
            pending_completion.append({"medida": medida_serializada})

    return Response({
        "success": True,
        "data": {
            "approved": approved,
            "pending_review": pending_review,
            "rejected": rejected,
            "pending_completion": pending_completion
        }
    })


@extend_schema(
    tags=["Usuarios"],
    summary="Subir documentos",
    description=(
        "Permite a un usuario subir los archivos requeridos para una medida.\n\n"
        "**Requisitos:**\n"
        "- Usuario debe estar aprobado y no ser administrador.\n"
        "- Los archivos deben enviarse en `multipart/form-data`.\n"
        "- Cada archivo debe enviarse como `doc_<id>`, donde `<id>` es el ID del documento requerido.\n\n"
        "**Ejemplo:**\n"
        "Si la medida tiene documentos con ID 1 y 2, se deben enviar:\n\n"
        "```\n"
        "doc_1: archivo.pdf\n"
        "doc_2: informe.xlsx\n"
        "```\n\n"
        "Consultar [/api/usuario/dashboard/](/api/docs#/Usuarios/usuario_dashboard_retrieve) para obtener los IDs requeridos."
    ),
    request=OpenApiTypes.OBJECT,
    responses={"success": bool, "message": str},
    examples=[
        OpenApiExample(
            name="Ejemplo subida de documentos",
            value={
                "doc_1": "(archivo .pdf)",
                "doc_2": "(archivo .xlsx)"
            },
            request_only=True,
            media_type="multipart/form-data"
        )
    ]
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsRegularApprovedUser])
@parser_classes([MultiPartParser])
def api_subir_documentos(request, medida_id):
    user = request.user
    medida = get_object_or_404(Medida, pk=medida_id)

    if medida.organismo != user.organismo:
        return Response({"success": False, "error": "No tienes permiso para esta medida."}, status=403)

    SerializerClass = generar_documentos_serializer(medida)

    if request.method == 'POST':
        serializer = SerializerClass(data=request.data, files=request.FILES)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=400)

        try:
            indicador = Indicador.objects.create(
                medida=medida,
                usuario=user,
                calculo_indicador=0,
                cumple_requisitos=False
            )
            for doc in medida.documentos_requeridos.all():
                field_name = f'doc_{doc.id}'
                file = serializer.validated_data.get(field_name)
                if file:
                    filename = default_storage.save(file.name, file)
                    DocumentoSubido.objects.create(
                        indicador=indicador,
                        documento_requerido=doc,
                        archivo=filename
                    )
            return Response({"success": True, "message": "Documentos subidos correctamente."}, status=200)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)

    return Response({"success": False, "error": "Método no permitido."}, status=405)