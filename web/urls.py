from django.urls import path
from web import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.home, name="home"),
    path("juego/<int:pk>/", views.game, name="game"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('games/', views.game_list, name='game_list'),

    path('perfil/', views.pagina_perfil, name='pagina_perfil')
]
