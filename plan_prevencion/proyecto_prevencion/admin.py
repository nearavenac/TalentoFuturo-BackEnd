from django.contrib import admin
from .models import OrganismoPublico, TiposMedidas, Medida, Indicador
admin.site.register(OrganismoPublico)
admin.site.register(TiposMedidas)
admin.site.register(Medida)
admin.site.register(Indicador)

# Register your models here.
