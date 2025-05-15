from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre

class Videojuego(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    genero = models.ManyToManyField(Genero)
    rating = models.FloatField(null=True, blank=True)
    portada = models.URLField(null=True, blank=True)  # URL de la portada

    def __str__(self):
        return self.titulo

class Review(models.Model):
    titulo = models.CharField('Título', max_length=255)
    rating = models.FloatField(null=True, blank=True)
    texto = models.TextField(null=True, blank=True)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)  # Permitimos múltiples reviews por juego
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    fecha_review = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.titulo

class CustomUser(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')
    juegos_guardados = models.ManyToManyField('Videojuego', blank=True)
    def __str__(self):
        return self.username