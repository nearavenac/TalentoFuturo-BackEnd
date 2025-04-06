# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from proyecto_prevencion.models import Usuario

class UsuarioRegistrationForm(UserCreationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'rut_usuario', 'organismo', 'password1', 'password2']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'rut_usuario': 'RUT del Usuario',
            'organismo': 'Organismo Público',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'rut_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'organismo': forms.Select(attrs={
                'class': 'selectpicker',
                'data-live-search': 'true',
            }),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'username': {
                'required': "Este campo es obligatorio.",
            },
            'first_name': {
                'required': "Este campo es obligatorio.",
            },
            'last_name': {
                'required': "Este campo es obligatorio.",
            },
            'rut_usuario': {
                'required': "Este campo es obligatorio.",
            },
            'organismo': {
                'required': "Este campo es obligatorio.",
            },
            'password1': {
                'required': "Este campo es obligatorio.",
            },
            'password2': {
                'required': "Este campo es obligatorio.",
            },
        }

def generar_subir_documentos_form(documentos):
    class SubirDocumentosForm(forms.Form):
        pass
    for doc in documentos:
        field_name = f'doc_{doc.id}'
        SubirDocumentosForm.base_fields[field_name] = forms.FileField(
            label=doc.descripcion,
            required=True,
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )
    return SubirDocumentosForm
