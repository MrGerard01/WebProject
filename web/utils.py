from datetime import datetime
import requests
from .models import Videojuego, Genero

CLIENT_ID = "9vfzl5tc1x9ekb58ahdtg14og1ecmp"
CLIENT_SECRET = "und6b4vuxn6alvmeaiqefcanhkt96o"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"
API_URL = "https://api.igdb.com/v4/games"


def obtener_token():
    """Obtiene un token de acceso para la API de IGDB"""
    response = requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    })
    return response.json().get("access_token")


def importar_juegos_desde_igdb():
    """Importa juegos desde IGDB y los guarda en la base de datos"""
    token = obtener_token()
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }

    query = """
        fields name, summary, first_release_date, aggregated_rating, genres.name, cover.url;
        where aggregated_rating > 40;
        limit 500;
    """

    response = requests.post(API_URL, headers=headers, data=query)

    if response.status_code == 200:
        data = response.json()
        for game in data:
            # Convertir la fecha de lanzamiento (si existe) de timestamp a datetime
            fecha_lanzamiento = game.get("first_release_date")
            if fecha_lanzamiento:
                try:
                    fecha_lanzamiento = datetime.fromtimestamp(fecha_lanzamiento)
                except ValueError:
                    fecha_lanzamiento = None  # Si hay un error al convertir la fecha, la dejamos como None

            # Obtener la URL completa de la imagen (si existe)
            imagen_url = game.get("cover", {}).get("url", "")
            if imagen_url:
                if not imagen_url.startswith("http"):
                    imagen_url = "https:" + imagen_url  # Completar la URL si es relativa
                if "t_thumb" in imagen_url:
                    imagen_url = imagen_url.replace("t_thumb", "t_1080p")  # Usar t_1080p si está disponible
                elif "t_cover_small" in imagen_url:
                    imagen_url = imagen_url.replace("t_cover_small", "t_1080p")

                # Crear los géneros o buscar los existentes
                generos = []
                for genre_data in game.get("genres", []):
                    genero_nombre = genre_data["name"]
                    genero, created = Genero.objects.get_or_create(nombre=genero_nombre)
                    generos.append(genero)

                # Usar update_or_create solo si la imagen existe
                videojuego, created = Videojuego.objects.update_or_create(
                    titulo=game.get("name"),
                    defaults={
                        'portada': imagen_url,
                        'fecha_lanzamiento': fecha_lanzamiento,
                        'rating': game.get("aggregated_rating"),
                        'descripcion': game.get("summary", "")
                    }
                )

                if created:
                    videojuego.genero.set(generos)  # Asignar los géneros a través de la relación ManyToMany
                    print(f"✅ Juego creado: {videojuego.titulo}")
                else:
                    videojuego.genero.set(generos)
                    print(f"🔄 Juego actualizado: {videojuego.titulo}")
            else:
                print(f"❌ Juego sin imagen: {game['name']} no se ha importado.")

        print("✅ Juegos importados o actualizados con éxito")
    else:
        print(f"❌ Error al obtener juegos: {response.status_code}")