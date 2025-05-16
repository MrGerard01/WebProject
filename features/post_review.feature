Feature: Reviews de videojuegos

  Scenario: Usuario agrega una review satisfactoriamente
    Given que estoy en la página del videojuego
    When ingreso una review con comentario "Juego increíble" y rating "5"
    Then debería ver la review "Juego increíble" en la página