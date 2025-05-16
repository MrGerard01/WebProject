Feature: Flujo completo de reviews

  Scenario: Flujo completo de reviews
    Given que estoy logueado con usuario "sdv" y contraseña "Bogdan"
    And que estoy en la página del videojuego
    When ingreso una review con título "Test Review" comentario "Muy bueno" y rating "8"
    Then debería ver la review "Muy bueno"
    When edito la review con título "Test Review" nuevo título "Hermoso" nuevo comentario "Excelente" y nuevo rating "9"
    Then debería ver la review "Excelente"
    When elimino la review con título "Hermoso"
    Then no debería ver la review "Excelente"
