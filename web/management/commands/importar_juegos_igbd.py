from django.core.management.base import BaseCommand
from web.utils import importar_juegos_desde_igdb

class Command(BaseCommand):
    help = "Importa videojuegos desde la API de IGDB"

    def handle(self, *args, **kwargs):
        importar_juegos_desde_igdb()