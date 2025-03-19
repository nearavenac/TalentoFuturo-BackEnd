from rest_framework import viewsets
from django.shortcuts import render
from .models import OrganismoPublico, TiposMedidas, Medida, Indicador, Usuario
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import OrganismoPublicoSerializer, TiposMedidasSerializer, MedidaSerializer, IndicadorSerializer, UsuarioSerializer

class OrganismoPublico(viewsets.ModelViewSet):
    """
    API para gestionar los organismos públicos

    Métodos:
    - GET /api/organismos/: listar todos los organismos
    - POST /api/organismos/: agregar un nuevo organismo
    - PUT /api/organismos/{id}: actualizar un organismo
    - DELETE /api/organismos/{id}: eliminar un organismo
    """
    queryset = OrganismoPublico.objects.all()
    serializer_class = OrganismoPublicoSerializer

class TiposMedidas(viewsets.ModelViewSet):
    """
    API para gestionar los tipos de medidas

    Métodos:
    - GET /api/tipos_medidas/: listar todos los tipos de medidas
    - POST /api/tipos_medidas/: agregar un nuevo tipo de medida
    - PUT /api/tipos_medidas/{id}: actualizar un tipo de medida
    - DELETE /api/tipos_medidas/{id}: eliminar un tipo de medida
    """
    queryset = TiposMedidas.objects.all()
    serializer_class = TiposMedidasSerializer

class Medida(viewsets.ModelViewSet):
    """
    API para gestionar las medidas

    Métodos:
    - GET /api/medidas/: listar todas las medidas
    - POST /api/medidas/: agregar una nueva medida
    - PUT /api/medidas/{id}: actualizar una medida
    - DELETE /api/medidas/{id}: eliminar una medida
    """
    queryset = Medida.objects.all()
    serializer_class = MedidaSerializer

class Indicador(viewsets.ModelViewSet):
    """
    API para gestionar los indicadores

    Métodos:
    - GET /api/indicadores/: listar todos los indicadores
    - POST /api/indicadores/: agregar un nuevo indicador
    - PUT /api/indicadores/{id}: actualizar un indicador
    - DELETE /api/indicadores/{id}: eliminar un indicador
    """
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer

class Usuario(viewsets.ModelViewSet):
    """
    API para gestionar los usuarios

    Métodos:
    - GET /api/usuarios/: listar todos los usuarios
    - POST /api/usuarios/: agregar un nuevo usuario
    - PUT /api/usuarios/{id}: actualizar un usuario
    - DELETE /api/usuarios/{id}: eliminar un usuario
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def home(request):
    """
    Pagina de inicio del sitio
    """
    return render(request, 'home.html')
