from django.core.management.base import BaseCommand
from common.utils import importar_juegos_desde_igbd

class Command(BaseCommand):
    help = "Importa videojuegos desde la API de IGDB"

    def handle(self, *args, **kwargs):
        importar_juegos_desde_igdb()