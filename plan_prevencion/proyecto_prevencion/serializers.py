from   rest_framework import serializers
from   .models import OrganismoPublico, TiposMedidas, Medida, Indicador, Usuario

class OrganismoPublicoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo OrganismoPublico

    Este serializar convierte instancias del modelo OrganismoPublico a representaciones JSON

    Atributos:
    - id_organismo(int): identificador único del organismo
    - nombre_organismo(str): nombre del organismo
    """
    class Meta:
        model = OrganismoPublico
        fields = '__all__'

class TiposMedidasSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TiposMedidas

    Este serializar convierte instancias del modelo TiposMedidas a representaciones JSON

    Atributos:
    - id_tipo_medida(int): identificador único del tipo de medida
    - nombre_tipo_medida(str): nombre del tipo de medida
    """
    class Meta:
        model = TiposMedidas
        fields = '__all__'

class MedidaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Medida

    Este serializar convierte instancias del modelo Medida a representaciones JSON

    Atributos:
    - id_medida(int): identificador único de la medida
    - id_tipo_medida(int): identificador del tipo de medida
    - nombre_largo(str): nombre largo de la medida
    - id_organismo(int): identificador del organismo al que pertenece la medida
    - regulatorio(bool): si la medida es regulatoria o no
    - tipo_formula(float): tipo de formula que se utiliza para calcular el indicador
    - datos_requeridos(str): datos requeridos para realizar la medida
    - formula(float): formula matemática para calcular el indicador
    - umbral_medida(float): umbral de la medida
    """
    class Meta:
        model = Medida
        fields = '__all__'

class IndicadorSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Indicador

    Este serializar convierte instancias del modelo Indicador a representaciones JSON

    Atributos:
    - id_indicador(int): identificador único del indicador
    - id_medida(int): identificador del tipo de medida
    - data(dict): datos del indicador
    - calculo_indicador(float): valor del indicador
    - cumple_requisitos(bool): si cumplen los requisitos para el indicador
    - fecha_reporte(date): fecha de reporte del indicador
    """
    class Meta:
        model = Indicador
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Usuario

    Este serializar convierte instancias del modelo Usuario a representaciones JSON

    Atributos:
    - id_usuario(int): identificador único del usuario
    - rut_usuario(str): rut del usuario
    - nombre_usuario(str): nombre del usuario
    - direccion(str): direccion del usuario
    - correo(str): correo electrónico del usuario
    - id_organismo(int): identificador del organismo al que pertenece el usuario
    """
    class Meta:
        model = Usuario
        fields = '__all__'