from django.urls import path
from web import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.home, name="home"),
    path('guardar-juego/<int:pk>/', views.guardar_juego, name='guardar_juego'),
    path('quitar-juego/<int:pk>/', views.quitar_juego, name='quitar_juego'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('games/', views.game_list, name='game_list'),
    path('perfil/', views.pagina_perfil, name='pagina_perfil'),
    path("juego/<int:pk>/", views.game, name="game"),
    path('review/<int:review_id>/eliminar/', views.eliminar_review, name='eliminar_review'),
    path('review/<int:review_id>/editar/', views.editar_review, name='editar_review'),
]
