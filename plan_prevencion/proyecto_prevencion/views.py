from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from rest_framework.decorators import api_view

def logout_view(request):
    logout(request)
    return redirect('home')

@api_view(['GET'])
def home(request):
    """
    Pagina de inicio del sitio
    """
    return render(request, 'home.html')
