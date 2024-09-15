from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .utils import user_is_authenticated
from api.models import User

def login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # Iniciar sesión con el usuario
                request.session['user_email'] = user.email
                return redirect('admin')
            else:
                # Contraseña incorrecta
                messages.error(request, 'Contraseña incorrecta')
                return render(request, 'dashboard/login.html', status=401)
        except User.DoesNotExist:
            # Usuario no encontrado
            messages.error(request, 'Usuario no encontrado')
            return render(request, 'dashboard/login.html', status=401)

    return render(request, 'dashboard/login.html')


@user_is_authenticated
def dashboard(request):
    user_email = request.session.get('user_email')
    return render(request,'dashboard/admin.html', {
        'user_email': user_email
    })

def redirect_to_login(request):
    return redirect('/dashboard/login/')
