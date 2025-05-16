from behave import when, given, then
import time


@given('que estoy logueado con usuario "{username}" y contraseña "{password}"')
def step_login(context, username, password):
    context.browser.visit("http://localhost:8000/login/")
    context.browser.fill("username", username)
    context.browser.fill("password", password)
    context.browser.find_by_value("Login").first.click()
    time.sleep(1)

@given('que estoy en la página del videojuego')
def step_go_to_game_page(context):
    context.browser.visit("http://localhost:8000/juego/1/")
    time.sleep(1)

@when('ingreso una review con título "{titulo}" comentario "{texto}" y rating "{rating}"')
def step_post_review(context, titulo, texto, rating):
    context.browser.fill("titulo", titulo)
    context.browser.fill("texto", texto)
    context.browser.fill("rating", rating)
    context.browser.find_by_text("Publicar reseña").first.click()
    time.sleep(1)

@then('debería ver la review "{texto}"')
def step_see_review(context, texto):
    assert context.browser.is_text_present(texto)
    time.sleep(1)

@when('edito la review con título "{titulo_original}" nuevo título "{nuevo_titulo}" nuevo comentario "{nuevo_texto}" y nuevo rating "{nuevo_rating}"')
def step_edit_review(context, titulo_original, nuevo_titulo, nuevo_texto, nuevo_rating):
    review_cards = context.browser.find_by_css("div.review-card")
    editar_button = None
    review_id = None

    for card in review_cards:
        title_element = card.find_by_css("h5.titulo")
        if title_element and titulo_original == title_element.first.text:
            editar_button = card.find_by_css("button[data-bs-toggle='modal']").first
            review_id = editar_button["data-bs-target"].split('-')[-1]
            break

    assert editar_button is not None, f"No se encontró la review con título '{titulo_original}' para editar"

    editar_button.click()
    time.sleep(1)

    modal_selector = f"#editarModal-{review_id}"
    modal = context.browser.find_by_css(modal_selector).first

    # Llenar el campo título si existe
    titulo_field = modal.find_by_name("titulo")
    if titulo_field:
        titulo_field.first.fill(nuevo_titulo)
    else:
        print("Advertencia: No se encontró el campo 'titulo'.")

    # Llenar el campo texto
    texto_field = modal.find_by_name("texto")
    assert texto_field, "No se encontró el campo 'texto'."
    texto_field.first.fill(nuevo_texto)

    # Llenar el campo rating
    rating_field = modal.find_by_name("rating")
    assert rating_field, "No se encontró el campo 'rating'."
    rating_field.first.fill(nuevo_rating)

    # Click en el botón de guardar
    guardar_button = modal.find_by_css("button.btn-success")
    assert guardar_button, "No se encontró el botón para guardar."
    guardar_button.first.click()

    time.sleep(1)

@when('elimino la review con título "{titulo}"')
def step_delete_review(context, titulo):
    review_cards = context.browser.find_by_css("div.review-card")
    deleted = False
    for card in review_cards:
        try:
            title_element = card.find_by_css("h5.titulo")
            if titulo == title_element.text:
                delete_button = card.find_by_css("button.btn-outline-danger").first
                delete_button.click()
                context.browser.driver.switch_to.alert.accept()  # Aceptar la alerta en Splinter
                time.sleep(1)
                deleted = True
                return
        except Exception as e:
            print(f"Error al intentar interactuar con la reseña: {e}")
            continue
    if not deleted:
        assert False, f"No se encontró la review con título '{titulo}' para eliminar"

@then('no debería ver la review "{texto}"')
def step_not_see_review(context, texto):
    assert not context.browser.is_text_present(texto)
