import requests
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView

from web.forms import CustomUserCreationForm, CustomUserChangeForm
from web.models import Videojuego, Genero, CustomUser


def home(request):
    API_KEY = 'pub_78670010e7e9dc763d072171bfec442ce08dc'
    URL = 'https://newsdata.io/api/1/news'

    noticias = []
    try:
        params = {
            'apikey': API_KEY,
            'q': 'videojuegos',
            'language': 'es',
            'category': 'technology',
        }
        response = requests.get(URL, params=params)
        response.raise_for_status()
        resultados = response.json().get('results', [])

        # Usamos un conjunto para almacenar títulos únicos
        titulos_vistos = set()
        noticias_unicas = []

        for noticia in resultados:
            titulo = noticia['title']

            if titulo not in titulos_vistos:
                titulos_vistos.add(titulo)
                noticias_unicas.append(noticia)

        noticias = noticias_unicas[:4]
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener noticias: {e}")
    except ValueError as e:
        print(f"Error al procesar los datos JSON: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    videojuegos = Videojuego.objects.all().order_by('-rating')[:6]

    return render(request, 'home.html', {
        'noticias': noticias,
        'videojuegos': videojuegos,
    })

def game(request, pk):
    juego = get_object_or_404(Videojuego, pk=pk)

    genero = juego.genero.first()
    print(genero)
    similares = (
        Videojuego.objects.filter(genero__nombre__icontains=genero).exclude(pk=juego.pk)[:6]
        if genero else []
    )

    print(similares)

    return render(request, "game.html", {
        "juego": juego,
        "similares": similares,
    })

def game_list(request, category=None):
    q = request.GET.get('q', '')
    page_number = request.GET.get('page')  # Página actual
    category = request.GET.get('category')

    # Todos los videojuegos ordenados por título
    videojuegos = Videojuego.objects.all().order_by('titulo')
    generos = Genero.objects.all().order_by('nombre')

    # Filtro por búsqueda
    if q:
        videojuegos = videojuegos.filter(titulo__startswith=q)
    if category:
        videojuegos = videojuegos.filter(genero__nombre__icontains=category)

    videojuegos = videojuegos.distinct()

    # Paginación (20 juegos por página)
    paginator = Paginator(videojuegos, 20)
    page_obj = paginator.get_page(page_number)

    # Parámetros actuales para mantenerlos en los enlaces de paginación
    filtros_get = request.GET.copy()
    if 'page' in filtros_get:
        filtros_get.pop('page')  # Quitamos el número de página para regenerarlo en los enlaces

    context = {
        'page_obj': page_obj,
        'generos': Genero.objects.all(),
        'genero_actual': category,
        'filtros_get': f"category={category}&q={q}" if category or q else "",
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/partial_list.html', context)
    return render(request, 'game_list.html', context)

class register_view(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "register.html"

@login_required
def pagina_perfil(request):
    user = request.user
    juegos_favoritos = user.juegos_guardados.all()
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('pagina_perfil')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'perfil.html', {'form': form, 'juegos': juegos_favoritos})