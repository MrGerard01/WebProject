from django.urls import path
from web import views

urlpatterns = [
    path("", views.home, name="home"),
    path("genero/<str:category>/", views.home, name="games_by_genre"),  # Ruta con género
    path("juego/<int:pk>/", views.game, name="game"),
]
