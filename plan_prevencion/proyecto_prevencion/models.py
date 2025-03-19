from django.db import models

# Create your models here.
class OrganismoPublico(models.Model):
    """
    Representa a un organismo público

    Atributos:
    - id_organismo(int): identificador único del organismo
    - nombre_organismo(str): nombre del organismo
    """
    id_organismo = models.AutoField(primary_key=True)
    nombre_organismo = models.CharField(max_length=100)
    only_admin =  models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_organismo

class TiposMedidas(models.Model):
    """
    Representa los tipos de medidas que se pueden realizar en el sistema

    Atributos:
    - id_tipo_medida(int): identificador único del tipo de medida
    - nombre_tipo_medida(str): nombre del tipo de medida
    """
    id_tipo_medida = models.AutoField(primary_key=True)
    nombre_tipo_medida = models.CharField(max_length=100)

class Medida(models.Model):
    """
    Representa una medida que se puede realizar en el sistema

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
    id_medida = models.AutoField(primary_key=True)
    id_tipo_medida = models.ForeignKey(TiposMedidas, on_delete=models.CASCADE)
    nombre_largo = models.CharField(max_length=100)
    id_organismo = models.ForeignKey(OrganismoPublico, on_delete=models.CASCADE)
    regulatorio = models.BooleanField(default=True)
    tipo_formula = models.FloatField()
    datos_requeridos = models.CharField(max_length=100)
    formula = models.FloatField()
    umbral_medida = models.FloatField()

class Indicador(models.Model):
    """
    Representa un indicador que se calcula a partir de las medidas realizadas

    Atributos:
    - id_indicador(int): identificador único del indicador
    - id_medida(int): identificador del tipo de medida
    - data(dict): datos del indicador
    - calculo_indicador(float): valor del indicador
    - cumple_requisitos(bool): si cumplen los requisitos para el indicador
    - fecha_reporte(date): fecha de reporte del indicador
    """
    id_indicador = models.AutoField(primary_key=True)
    id_medida = models.ForeignKey(Medida, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)
    calculo_indicador = models.FloatField()
    cumple_requisitos = models.BooleanField(default=True)
    fecha_reporte = models.DateField(auto_now_add=True)

class Usuario(models.Model):
    """
    Representa un usuario del sistema

    Atributos:
    - id_usuario(int): identificador único del usuario
    - rut_usuario(str): rut del usuario
    - nombre_usuario(str): nombre del usuario
    - direccion(str): direccion del usuario
    - correo(str): correo electrónico del usuario
    - id_organismo(int): identificador del organismo al que pertenece el usuario
    """
    id_usuario = models.AutoField(primary_key=True)
    rut_usuario = models.CharField(unique=True, blank=True, null=True, max_length=10)
    nombre_usuario = models.CharField(max_length=50)
    direccion = models.CharField(blank=True, null=True, max_length=100)
    correo = models.EmailField(max_length=50)
    id_organismo = models.ForeignKey(OrganismoPublico, on_delete=models.CASCADE)
