document.addEventListener("DOMContentLoaded", function() {
    let page = 1; // Página inicial para la carga de más juegos
    const loadingIndicator = document.getElementById('loading');
    const loadingBar = document.getElementById('loading-bar');
    const gameList = document.getElementById('game-list');
    let loading = false;

    // Obtener los parámetros iniciales desde la URL
    const urlParams = new URLSearchParams(window.location.search);
    let q = urlParams.get('q') || '';
    let orden = urlParams.get('orden') || '';

    const buildUrl = (pageNumber) => {
        const params = new URLSearchParams();

        if (q) params.set('q', q);
        if (orden) params.set('orden', orden);

        params.set('page', pageNumber);

        return `/web2/all_list/?${params.toString()}`;
    };

    // Función para cargar más juegos
    const loadMoreGames = () => {
        if (loading) return; // Evitar múltiples solicitudes simultáneas
        loading = true;
        loadingIndicator.style.visibility = 'visible';
        loadingBar.style.width = '0%';

        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            loadingBar.style.width = `${progress}%`;
            if (progress >= 100) clearInterval(interval);
        }, 200);

        // Retraso para simular carga
        setTimeout(() => {
            const url = buildUrl(page);
            fetch(url)
                .then(response => response.text())
                .then(data => {
                    const newGames = new DOMParser().parseFromString(data, 'text/html').getElementById('game-list').innerHTML;

                    if (newGames.trim() === '') {
                        // No hay más juegos, dejar de observar
                        observer.unobserve(loadingIndicator);
                        loadingIndicator.style.visibility = 'hidden';
                    } else {
                        gameList.innerHTML += newGames;
                        page++;
                    }

                    loadingIndicator.style.visibility = 'hidden';
                    loading = false;
                })
                .catch(error => {
                    console.error('Error al cargar juegos:', error);
                    loadingIndicator.style.visibility = 'hidden';
                    loading = false;
                    alert('Hubo un error al cargar los juegos. Por favor, intenta nuevamente.');
                });
        }, 2000);
    };

    // IntersectionObserver para cargar más juegos cuando el indicador es visible
    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) {
            loadMoreGames();
        }
    }, { threshold: 1.0 });

    observer.observe(loadingIndicator);

    // Cargar la primera página al iniciar
    loadMoreGames();

    // Manejar cambios en la búsqueda para reiniciar la lista
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Obtener los valores de los campos del formulario
            q = filterForm.querySelector('input[name="q"]').value;
            orden = filterForm.querySelector('select[name="orden"]').value;

            // Cambiar URL en la barra de direcciones (opcional)
            const newUrl = buildUrl(1);
            window.history.pushState({}, '', newUrl);

            // Reiniciar lista y paginación
            gameList.innerHTML = '';
            page = 1;

            // Volver a observar por si se detuvo
            observer.observe(loadingIndicator);

            // Cargar la primera tanda de resultados
            loadMoreGames()
        });
    }
});