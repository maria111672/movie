let currentView = "home";
let currentCategory = "";
let currentSearch = "";
let favorites = new Set();

async function init() {
    await loadCategories();
    //await loadStats();
    await loadMovies();
    await loadFavorites();

    document.getElementById("searchInput").addEventListener("keydown", (e) => {
        if (e.key === "Enter") performSearch();
    });
}

async function loadCategories() {
    const res = await fetch("/api/categories");
    const categories = await res.json();
    const container = document.getElementById("categoryChips");
    container.innerHTML = '<button class="chip active" data-category="" onclick="filterByCategory(\'\')">All</button>';
    categories.forEach((cat) => {
        const btn = document.createElement("button");
        btn.className = "chip";
        btn.dataset.category = cat;
        btn.textContent = cat;
        btn.onclick = () => filterByCategory(cat);
        container.appendChild(btn);
    });
}

async function loadStats() {
    const res = await fetch("/api/stats");
    const stats = await res.json();
    document.getElementById("statMovies").textContent = stats.total_movies;
    document.getElementById("statCategories").textContent = stats.total_categories;
    document.getElementById("statRating").textContent = stats.avg_rating;
}

async function loadFavorites() {
    const res = await fetch("/api/favorites");
    const favs = await res.json();
    favorites = new Set(favs.map((m) => m.id));
    updateFavCount();
}

async function loadMovies() {
    const grid = document.getElementById("moviesGrid");
    const empty = document.getElementById("emptyState");
    const spinner = document.getElementById("loadingSpinner");

    spinner.style.display = "flex";
    grid.innerHTML = "";
    empty.style.display = "none";

    const params = new URLSearchParams();
    if (currentSearch) params.set("q", currentSearch);
    if (currentCategory) params.set("category", currentCategory);

    const sort = document.getElementById("sortSelect").value;
    if (sort) params.set("sort", sort);

    const res = await fetch("/api/movies?" + params.toString());
    const movies = await res.json();

    spinner.style.display = "none";

    if (movies.length === 0) {
        empty.style.display = "block";
        return;
    }

    movies.forEach((movie) => {
        grid.appendChild(createMovieCard(movie));
    });
}

function createMovieCard(movie) {
    const card = document.createElement("div");
    card.className = "movie-card";
    card.onclick = (e) => {
        if (e.target.closest(".fav-btn")) return;
        openModal(movie.id);
    };

    const isFav = favorites.has(movie.id);

    card.innerHTML = `
        <button class="fav-btn ${isFav ? "active" : ""}" onclick="toggleFavorite(${movie.id}, this, event)" title="Toggle favorite">
            ${isFav ? "&#9829;" : "&#9825;"}
        </button>
        <img class="movie-poster" src="${movie.poster}" alt="${movie.title}" onerror="this.outerHTML='<div class=\\'movie-poster-placeholder\\'>&#127916;</div>'" loading="lazy">
        <div class="movie-info">
            <div class="movie-title" title="${movie.title}">${movie.title}</div>
            <div class="movie-meta">
                <span class="movie-category-badge">${movie.category}</span>
                <span class="movie-rating">&#9733; ${movie.rating}</span>
            </div>
            <div class="movie-meta" style="margin-top:6px;">
                <span>${movie.year}</span>
            </div>
        </div>
    `;

    return card;
}

function navigateTo(view) {
    currentView = view;
    currentCategory = "";
    currentSearch = "";
    document.getElementById("searchInput").value = "";
    document.getElementById("sortSelect").value = "";

    document.querySelectorAll(".nav-link").forEach((l) => l.classList.remove("active"));
    document.querySelector(`.nav-link[data-view="${view}"]`).classList.add("active");

    const filters = document.getElementById("filtersSection");
    const statsBar = document.getElementById("statsBar");

    if (view === "favorites") {
        filters.style.display = "none";
        statsBar.style.display = "none";
        loadFavoritesView();
    } else {
        filters.style.display = "flex";
        statsBar.style.display = "flex";
        resetCategoryChips();
        loadMovies();
    }
}

async function loadFavoritesView() {
    const grid = document.getElementById("moviesGrid");
    const empty = document.getElementById("emptyState");
    grid.innerHTML = "";
    empty.style.display = "none";

    const res = await fetch("/api/favorites");
    const movies = await res.json();

    if (movies.length === 0) {
        empty.style.display = "block";
        empty.querySelector("h2").textContent = "No favorites yet";
        empty.querySelector("p").textContent = "Click the heart icon on movies to add them to your favorites";
        return;
    }

    movies.forEach((movie) => {
        grid.appendChild(createMovieCard(movie));
    });
}

function filterByCategory(category) {
    currentCategory = category;

    document.querySelectorAll(".chip").forEach((c) => {
        c.classList.toggle("active", c.dataset.category === category);
    });

    loadMovies();
}

function resetCategoryChips() {
    document.querySelectorAll(".chip").forEach((c) => {
        c.classList.toggle("active", c.dataset.category === "");
    });
}

async function performSearch() {
    const query = document.getElementById("searchInput").value.trim();

    if (!query) {
        loadMovies();
        return;
    }

    const res = await fetch(`/api/tmdb-search?q=${encodeURIComponent(query)}`);
    const data = await res.json();

    const grid = document.getElementById("moviesGrid");
    const empty = document.getElementById("emptyState");
    const spinner = document.getElementById("loadingSpinner");

    spinner.style.display = "flex";
    grid.innerHTML = "";
    empty.style.display = "none";

    const movies = data.results || [];

    spinner.style.display = "none";

    if (movies.length === 0) {
        empty.style.display = "block";
        return;
    }

    movies.forEach((movie) => {
        const card = document.createElement("div");
        card.className = "movie-card";

        const poster = movie.poster_path
            ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
            : "";

        card.innerHTML = `
            <img class="movie-poster"
                 src="${poster}"
                 alt="${movie.title}"
                 onerror="this.outerHTML='<div class=\\'movie-poster-placeholder\\'>&#127916;</div>'">

            <div class="movie-info">
                <div class="movie-title">${movie.title}</div>

                <div class="movie-meta">
                    <span>
                        ${movie.release_date
                            ? movie.release_date.substring(0, 4)
                            : "Unknown"}
                    </span>

                    <span class="movie-rating">
                        &#9733;
                        ${movie.vote_average
                            ? movie.vote_average.toFixed(1)
                            : "N/A"}
                    </span>
                </div>
            </div>
        `;

        card.onclick = () => {
            openTMDBModal(movie);
        };

        grid.appendChild(card);
    });
}


function openTMDBModal(movie) {
    const modal = document.getElementById("movieModal");
    const body = document.getElementById("modalBody");

    const poster = movie.poster_path
        ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
        : "";

    const year = movie.release_date
        ? movie.release_date.substring(0, 4)
        : "Unknown";

    body.innerHTML = `
        <div class="modal-hero">
            <img src="${poster}" alt="${movie.title}">
            <div class="modal-hero-gradient"></div>

            <div class="modal-hero-content">
                <img
                    class="modal-poster"
                    src="${poster}"
                    alt="${movie.title}"
                >

                <div class="modal-hero-info">
                    <h1>${movie.title}</h1>

                    <div class="modal-hero-meta">
                        <span>${year}</span>
                        <span>&#9733; ${movie.vote_average.toFixed(1)}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal-content">

            <div class="modal-section">
                <h3>Rating</h3>
                <p>&#9733; ${movie.vote_average.toFixed(1)} / 10</p>
            </div>

            <div class="modal-section">
                <h3>Synopsis</h3>
                <p>
                    ${movie.overview || "No description available."}
                </p>
            </div>

            <div class="modal-section">
                <h3>Release Year</h3>
                <p>${year}</p>
            </div>

        </div>
    `;

    modal.classList.add("open");
    document.body.style.overflow = "hidden";
}


function applyFilters() {
    loadMovies();
}

async function toggleFavorite(movieId, btn, event) {
    event.stopPropagation();
    const res = await fetch(`/api/favorites/${movieId}`, { method: "POST" });
    const data = await res.json();

    if (data.favorited) {
        favorites.add(movieId);
        btn.classList.add("active");
        btn.innerHTML = "&#9829;";
    } else {
        favorites.delete(movieId);
        btn.classList.remove("active");
        btn.innerHTML = "&#9825;";
    }

    updateFavCount();

    if (currentView === "favorites") {
        loadFavoritesView();
    }
}

function updateFavCount() {
    document.getElementById("favCount").textContent = favorites.size;
}

async function openModal(movieId) {
    const res = await fetch(`/api/movies/${movieId}`);
    const movie = await res.json();
    const modal = document.getElementById("movieModal");
    const body = document.getElementById("modalBody");

    const fullStars = Math.floor(movie.rating / 2);
    const halfStar = movie.rating % 2 >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;

    let starsHTML = "";
    for (let i = 0; i < fullStars; i++) starsHTML += '<span class="star filled">&#9733;</span>';
    if (halfStar) starsHTML += '<span class="star half">&#9733;</span>';
    for (let i = 0; i < emptyStars; i++) starsHTML += '<span class="star">&#9733;</span>';

    body.innerHTML = `
        <div class="modal-hero">
            <img src="${movie.poster}" alt="${movie.title}" onerror="this.style.display='none'">
            <div class="modal-hero-gradient"></div>
            <div class="modal-hero-content">
                <img class="modal-poster" src="${movie.poster}" alt="${movie.title}" onerror="this.outerHTML='<div class=\\'modal-poster-placeholder\\'>&#127916;</div>'">
                <div class="modal-hero-info">
                    <h1>${movie.title}</h1>
                    <div class="modal-hero-meta">
                        <span class="movie-category-badge">${movie.category}</span>
                        <span>${movie.year}</span>
                        <span>${movie.duration}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal-content">
        <div class="modal-section">
    <h3>Watch Movie</h3>

    <video class="movie-player" controls>
        <source src="${movie.video}" type="video/mp4">
        Your browser does not support video playback.
    </video>
</div>
            <div class="modal-section">
                <h3>Rating</h3>
                <div class="rating-bar">
                    <span class="rating-number">${movie.rating}</span>
                    <div class="rating-stars">${starsHTML}</div>
                </div>
            </div>
            <div class="modal-section">
                <h3>Synopsis</h3>
                <p>${movie.description}</p>
            </div>
            <div class="modal-section">
                <h3>Director</h3>
                <p>${movie.director}</p>
            </div>
            <div class="modal-section">
                <h3>Cast</h3>
                <div class="modal-cast">
                    ${movie.cast.map((c) => `<span class="cast-chip">${c}</span>`).join("")}
                </div>
            </div>
            <div class="modal-actions">
                <button class="modal-fav-btn ${movie.favorited ? "active" : ""}" onclick="toggleModalFavorite(${movie.id}, this)">
                    ${movie.favorited ? "&#9829; Favorited" : "&#9825; Add to Favorites"}
                </button>
            </div>
        </div>
    `;

    modal.classList.add("open");
    document.body.style.overflow = "hidden";
}

function closeModal(event) {
    if (event.target === event.currentTarget) closeModalDirect();
}

function closeModalDirect() {
    document.getElementById("movieModal").classList.remove("open");
    document.body.style.overflow = "";
}

async function toggleModalFavorite(movieId, btn) {
    const res = await fetch(`/api/favorites/${movieId}`, { method: "POST" });
    const data = await res.json();

    if (data.favorited) {
        favorites.add(movieId);
        btn.classList.add("active");
        btn.innerHTML = "&#9829; Favorited";
    } else {
        favorites.delete(movieId);
        btn.classList.remove("active");
        btn.innerHTML = "&#9825; Add to Favorites";
    }

    updateFavCount();
    loadMovies();
}

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModalDirect();
});

init();
