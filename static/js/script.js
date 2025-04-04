document.addEventListener("DOMContentLoaded", function() {
    document.body.addEventListener("click", function(event) {
        // Asegúrate de que el clic es en un botón de paginación
        if (event.target.classList.contains("page-button")) {
            event.preventDefault();
            let page = event.target.getAttribute("data-page");
            let tipo = event.target.getAttribute("data-type"); // 'juegos' o 'shooters'
            let url;

            // Ajustar la URL dependiendo del tipo de contenido
            if (tipo === "shooters") {
                url = `?page_shoot=${page}`;
            } else if (tipo === "antiguos") {
                url = `?page_antiguos=${page}`;
            } else {
                url = `?page=${page}`;
            }

            // Realizar la solicitud AJAX
            fetch(url, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
                .then(response => response.json())
                .then(data => {
                    // Actualizar el contenido según el tipo
                    if (tipo === "shooters") {
                        document.getElementById("shooters-list").innerHTML = data.html;
                    } else if (tipo === "antiguos") {
                        document.getElementById("antiguos-list").innerHTML = data.html;
                    } else {
                        document.getElementById("juegos-list").innerHTML = data.html;
                    }
                })
                .catch(error => console.error("Error en AJAX:", error));
        }
    });
});