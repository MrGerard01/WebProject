from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify

from web.models import Videojuego, Genero
def home(request, category=None):
    """Lista de videojuegos, filtrados por género si se proporciona uno"""

    print(f"Category recibido en slug: {category}")

    videojuegos = Videojuego.objects.all().order_by('titulo')
    generos = Genero.objects.all()

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

    game_pagination = Paginator(videojuegos, 32)
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