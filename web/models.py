from django.contrib.auth.models import User
from django.db import models

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

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    email = models.CharField('Correo', max_length=100)
    contrasena = models.CharField('Contrasena', max_length=100)
    avatar = models.ImageField(null=True, blank=True)
    juegos_guardados = models.ManyToManyField(Videojuego, blank=True)
    def __str__(self):
        return self.usuario.username

class Review(models.Model):
    titulo = models.CharField('Título', max_length=255)
    rating = models.FloatField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)  # Permitimos múltiples reviews por juego
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_review = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.titulo