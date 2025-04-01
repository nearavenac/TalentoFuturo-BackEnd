from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def require_permission(condition, redirect_url='home', error_message="No cuenta con los permisos necesarios."):
    """
    Decorador que verifica una condición sobre request.user. Si no se cumple,
    redirige a 'redirect_url' y agrega un mensaje de error.
    La condición debe ser una función que reciba el usuario y retorne True si cumple, o False en caso contrario.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not condition(request.user):
                messages.error(request, error_message)
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
