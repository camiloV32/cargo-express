from django.shortcuts import redirect
from api.models import User

def user_is_authenticated(function):
    def wrap(request, *args, **kwargs):
        user_email = request.session.get('user_email')  # Obtener el user_id de la sesión
        if user_email:
            try:
                request.user = User.objects.get(email=user_email)
                return function(request, *args, **kwargs)
            except User.DoesNotExist:
                pass
        # Redirigir al login si no está autenticado
        return redirect('login')  
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
