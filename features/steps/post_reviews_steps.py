from behave import given, when, then
from splinter import Browser
import time

# Cambia esta URL base según tu entorno
BASE_URL = 'http://localhost:8000'

@given('que estoy en la página del videojuego')
def step_go_to_game_page(context):
    context.browser = Browser('chrome')
    game_pk = 1
    url = f'{BASE_URL}/game/{game_pk}/'
    context.browser.visit(url)
    time.sleep(1)

@when('ingreso una review con comentario "{comment}" y rating "{rating}"')
def step_fill_review_form(context, comment, rating):
    context.browser.fill('floatingTitulo', 'Reseña de prueba')
    context.browser.fill('floatingContenido', comment)
    context.browser.fill('floatingPuntuacion', rating)
    context.browser.find_by_value('Publicar reseña').first.click()
    time.sleep(1)

@then('debería ver la review "{comment}" en la página')
def step_check_review(context, comment):
    assert comment in context.browser.html
    context.browser.quit()