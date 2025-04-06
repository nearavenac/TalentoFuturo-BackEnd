from rest_framework import serializers
from proyecto_prevencion.models import OrganismoPublico, ComunaPlan, TiposMedidas, Medida, DocumentoRequerido, Indicador, DocumentoSubido, Usuario

class OrganismoPublicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoPublico
        fields = '__all__'

class ComunaPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComunaPlan
        fields = '__all__'

class TiposMedidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposMedidas
        fields = '__all__'

class DocumentoRequeridoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoRequerido
        fields = '__all__'

class MedidaSerializer(serializers.ModelSerializer):
    documentos_requeridos = DocumentoRequeridoSerializer(many=True, read_only=True)

    tipo_medida = serializers.PrimaryKeyRelatedField(
        queryset=TiposMedidas.objects.all()
    )
    organismo = serializers.PrimaryKeyRelatedField(
        queryset=OrganismoPublico.objects.all()
    )
    
    class Meta:
        model = Medida
        fields = '__all__'

class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = '__all__'

class DocumentoSubidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoSubido
        fields = '__all__'

class RechazoIndicadorSerializer(serializers.Serializer):
    motivo = serializers.CharField(help_text="Motivo del rechazo", required=True)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class UsuarioRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'rut_usuario', 'organismo']

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            rut_usuario=validated_data.get('rut_usuario'),
            organismo=validated_data.get('organismo'),
            aprobado=False
        )
        return user
    
def generar_documentos_serializer(medida):
    campos = {}
    for doc in medida.documentos_requeridos.all():
        field_name = f'doc_{doc.id}'
        campos[field_name] = serializers.FileField(
            required=True,
            help_text=doc.descripcion,
            label=doc.descripcion
        )

    return type(
        f'DocumentoSubidoSerializerMedida{medida.id}',
        (serializers.Serializer,),
        campos
    )

class IndicadorEstadoSerializer(serializers.Serializer):
    medida = MedidaSerializer()
    indicador_id = serializers.IntegerField(required=False)
    cumple_requisitos = serializers.BooleanField(required=False)
    fecha_reporte = serializers.DateTimeField(required=False)

class DashboardDataSerializer(serializers.Serializer):
    approved = IndicadorEstadoSerializer(many=True)
    pending_review = IndicadorEstadoSerializer(many=True)
    rejected = IndicadorEstadoSerializer(many=True)
    pending_completion = IndicadorEstadoSerializer(many=True)

class DashboardResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    data = DashboardDataSerializer()