const movies = window.appMovies || [];
const container = document.getElementById("movieList");

function createCard(movie) {
    const div = document.createElement("div");
    div.className = "card";
    div.dataset.title = movie;
    div.innerHTML = `
        <div class="movie-title">${movie}</div>
        <div class="movie-overview">Hover to see overview</div>
    `;
    div.onclick = () => {
        console.log('card clicked:', movie);
        openMovie(movie);
    };
    div.addEventListener("mouseenter", () => showOverview(div, movie));
    return div;
}

function showOverview(card, movie) {
    const overviewBox = card.querySelector(".movie-overview");
    if (overviewBox.dataset.loaded === "true") {
        return;
    }
    overviewBox.textContent = "Loading overview...";
    fetch(`/movie/${encodeURIComponent(movie)}`)
        .then(response => response.json())
        .then(data => {
            overviewBox.dataset.loaded = "true";
            overviewBox.textContent = data.overview || "Overview not available.";
        })
        .catch(() => {
            overviewBox.textContent = "Overview not available.";
        });
}

function renderCards(list) {
    container.innerHTML = "";
    list.forEach(movie => {
        container.appendChild(createCard(movie));
    });
}

movies.forEach(movie => {
    container.appendChild(createCard(movie));
});

function filterMovies() {
    let query = document.getElementById("searchInput").value.toLowerCase().trim();
    container.innerHTML = "";
    let filtered = movies.filter(movie => movie.toLowerCase().includes(query));
    if (query === "" || filtered.length === 0) {
        filtered = movies;
    }
    filtered.forEach(movie => {
        container.appendChild(createCard(movie));
    });
}

document.getElementById("searchBtn").onclick = filterMovies;
document.getElementById("searchInput").addEventListener("keydown", event => {
    if (event.key === "Enter") filterMovies();
});

async function openMovie(movie) {
    console.log('openMovie called for', movie);
    const modal = document.getElementById("modal");
    if (!modal) {
        console.error('modal element not found');
        return;
    }
    try {
        modal.classList.add("show");
        // prevent background scrolling while modal open
        try { document.body.style.overflow = 'hidden'; } catch (e) {}
    } catch (e) {
        console.error('error showing modal', e);
    }
    let res1;
    let data1;
    try {
        res1 = await fetch(`/movie/${encodeURIComponent(movie)}`);
        data1 = await res1.json();
    } catch (err) {
        console.error('fetch /movie error', err);
        document.getElementById("movieDetails").innerHTML = '<p>Failed to load movie details.</p>';
        return;
    }
    document.getElementById("movieDetails").innerHTML = `
        <h2>${data1.title}</h2>
        <p><b>Genres:</b> ${data1.genres}</p>
        <p><b>Director:</b> ${data1.director}</p>
        <p><b>Cast:</b> ${data1.cast}</p>
        <p>${data1.overview}</p>
        <p><b>Release:</b> ${data1.release_date}</p>
    `;
    let res2 = await fetch(`/recommend/${encodeURIComponent(movie)}`);
    let data2 = await res2.json();
    let html = "<h3>Recommended Movies</h3>";
    data2.recommendations.forEach(m => {
        html += `<p>- ${m}</p>`;
    });
    document.getElementById("recommendations").innerHTML = html;
}

function closeModal() {
    const modal = document.getElementById("modal");
    console.log('closeModal called');
    if (modal) modal.classList.remove("show");
    try { document.body.style.overflow = ''; } catch (e) {}
}
