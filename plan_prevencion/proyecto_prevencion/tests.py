from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Usuario, OrganismoPublico

# Create your tests here.
class TestUsuario(APITestCase):
    def setUp(self):
        # Crea un objeto Usuario en la base de datos con los detalles especificados
        self.organimos = OrganismoPublico.objects.create(nombre_organismo="Talento Futuro")
        self.usuario = Usuario.objects.create(
            rut_usuario="15637908-1",
            nombre_usuario="Giselle Fernandez",
            direccion="Av. Troncal San Francisco",
            correo="gisellefernandez@gmail.com",
            id_organismo=self.organimos
        )
        self.usuario.save()

    def test_create_usuario(self):
        #obtiene la URl para la vista
        url = reverse("usuario-list")
        data = {
            "rut_usuario": "15637908-2",
            "nombre_usuario": "Giselle Fernandez",
            "direccion": "Av. Troncal San Francisco",
            "correo": "gisellefernandez@gmail.com",
            "id_organismo": self.organimos.id_organismo
        }
        response = self.client.post(url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_usuario(self):
        url = reverse("usuario-detail", kwargs={"pk": self.usuario.id_usuario})
        response = self.client.get(url)
        # Comprueba que el status code sea 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestOrganismoPublico(APITestCase):
    def test_create_organismo(self):
        url = reverse("organismopublico-list")
        data = {
            "nombre_organismo": "Talento Futuro"
        }
        response = self.client.post(url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrganismoPublico.objects.get().nombre_organismo, "Talento Futuro")