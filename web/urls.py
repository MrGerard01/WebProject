from django.urls import path
from web import views

urlpatterns = [
    path("", views.home, name="home"),
    path("genero/<str:category>/", views.home, name="games_by_genre"),  # Ruta con género
    path("juego/<int:pk>/", views.game, name="game"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
