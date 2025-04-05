from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from web.forms import AuthenticationForm, RegistrationForm
from web.models import Videojuego, Genero, Usuario


def home(request, category=None):
    """Lista de videojuegos, filtrados por género si se proporciona uno"""
    videojuegos = Videojuego.objects.all().order_by('titulo')
    generos = Genero.objects.all()

    videojuegos, category = filtrar_genero(videojuegos, category, generos)

    game_pagination = Paginator(videojuegos, 20)
    page_number = request.GET.get('page')
    page_obj = game_pagination.get_page(page_number)

    return render(request, "home.html", {
        "page_obj": page_obj,
        "generos": generos,
        "genero_actual": category,
    })

def game(request, pk):
    juego = get_object_or_404(Videojuego, pk=pk)
    return render(request, "game.html", {"juego": juego})

def game_list(request, category=None):
    query = request.GET.get('q')  # Obtiene lo que el usuario escribió

    videojuegos = Videojuego.objects.all().order_by('titulo')
    generos = Genero.objects.all().order_by('nombre')

    if query:
        videojuegos = Videojuego.objects.filter(titulo__icontains=query)

    videojuegos, category = filtrar_genero(videojuegos, category, generos)

    game_pagination = Paginator(videojuegos, 20)
    page_number = request.GET.get('page')
    page_obj = game_pagination.get_page(page_number)

    return render(request, 'Game_list.html', {
        'page_obj': page_obj,
        "generos": generos,
        'query': query,
        "genero_actual": category,
    })

def filtrar_genero(videojuegos, category, generos):
    if category:
        try:
            # Buscar en la base de datos el género con el slug coincidente
            genero = next((g for g in generos if slugify(g.nombre) == category), None)
            if genero:
                videojuegos = videojuegos.filter(genero=genero)
                category = genero.nombre  # Restaurar el nombre original del género
            else:
                videojuegos = Videojuego.objects.none()
        except Exception as e:
            print(f"Error al buscar género: {e}")
            videojuegos = Videojuego.objects.none()
    return videojuegos, category

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirige a la página de inicio o cualquier URL que desees
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Guardamos el usuario
            user = form.save()

            Usuario.objects.create(usuario=user, email=user.email)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('home')