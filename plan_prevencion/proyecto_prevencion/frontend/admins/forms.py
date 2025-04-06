# admins/forms.py
import json
from django import forms
from proyecto_prevencion.models import OrganismoPublico, ComunaPlan, TiposMedidas, Medida, DocumentoRequerido

class OrganismoForm(forms.ModelForm):
    class Meta:
        model = OrganismoPublico
        fields = ['nombre_organismo']
        labels = {'nombre_organismo': 'Nombre del Organismo'}
        widgets = {
            'nombre_organismo': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            })
        }

class ComunaForm(forms.ModelForm):
    class Meta:
        model = ComunaPlan
        fields = ['nombre_comuna']
        labels = {'nombre_comuna': 'Nombre de la Comuna'}
        widgets = {
            'nombre_comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            })
        }

class TiposMedidasForm(forms.ModelForm):
    class Meta:
        model = TiposMedidas
        fields = ['nombre_tipo_medida']
        labels = {'nombre_tipo_medida': 'Nombre del Tipo de Medida'}
        widgets = {
            'nombre_tipo_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            })
        }

class MedidaForm(forms.ModelForm):
    datos_requeridos = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Medida
        fields = [
            'tipo_medida',
            'nombre_corto',
            'nombre_largo',
            'organismo',
            'regulatorio',
            'descripcion_formula',
            'tipo_formula',
            'frecuencia',
            'datos_requeridos'
        ]
        widgets = {
            'tipo_medida': forms.Select(attrs={'class': 'form-control'}),
            'nombre_corto': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_largo': forms.TextInput(attrs={'class': 'form-control'}),
            'organismo': forms.Select(attrs={
                'class': 'selectpicker',
                'data-live-search': 'true',
            }),
            'regulatorio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion_formula': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_formula': forms.Select(attrs={'class': 'form-control'}),
            'frecuencia': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(MedidaForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            docs = [doc.descripcion for doc in self.instance.documentos_requeridos.all()]
            self.initial['datos_requeridos'] = json.dumps(docs)
        else:
            self.initial['datos_requeridos'] = json.dumps([])
    
    def save(self, commit=True):
        instance = super().save(commit=commit)
        # Leer la lista de documentos desde el campo oculto
        data_str = self.cleaned_data.get('datos_requeridos', '[]')
        try:
            docs_list = json.loads(data_str)  # Se espera una lista de strings
        except Exception:
            docs_list = []
        
        instance.documentos_requeridos.all().delete()
        for desc in docs_list:
            if desc.strip():
                DocumentoRequerido.objects.create(
                    medida=instance,
                    descripcion=desc.strip()
                )
        return instance