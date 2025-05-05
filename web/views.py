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
    query = request.GET.get('q')  # Obtiene lo que el usuario escribió

    videojuegos = Videojuego.objects.all().order_by('titulo')
    generos = Genero.objects.all().order_by('nombre')

    if query:
        videojuegos = Videojuego.objects.filter(titulo__startswith=query)

    videojuegos, category = filtrar_genero(videojuegos, category, generos)

    game_pagination = Paginator(videojuegos, 20)
    page_number = request.GET.get('page')
    page_obj = game_pagination.get_page(page_number)

    return render(request, 'game_list.html', {
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