const filterButtons = document.querySelectorAll(".filter-btn");
const dishRows = document.querySelectorAll(".dish-row");
const searchInput = document.getElementById("dishSearch");

let currentRegion = "all";


/* =========================
   REGION FILTER
========================= */

filterButtons.forEach(button => {

    button.addEventListener("click", () => {

        // Remove active from all buttons
        filterButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        // Make clicked button active
        button.classList.add("active");

        // Get selected region
        currentRegion = button.dataset.region;

        filterDishes();

    });

});


/* =========================
   SEARCH
========================= */

searchInput.addEventListener("input", () => {

    filterDishes();

});


/* =========================
   FILTER FUNCTION
========================= */

function filterDishes() {

    const searchText = searchInput.value.toLowerCase().trim();

    dishRows.forEach(row => {

        const rowRegion = row.dataset.region;
        const dishName = row.querySelector("h2").textContent.toLowerCase();
        const location = row.querySelector("p").textContent.toLowerCase();

        const matchesRegion =
            currentRegion === "all" ||
            rowRegion === currentRegion;

        const matchesSearch =
            dishName.includes(searchText) ||
            location.includes(searchText);


        if (matchesRegion && matchesSearch) {

            row.style.display = "grid";

        } else {

            row.style.display = "none";

        }

    });

}

const params = new URLSearchParams(window.location.search);
const regionFromUrl = params.get("region");

if (regionFromUrl) {

    const selectedFilter = document.querySelector(
        `.filter-btn[data-region="${regionFromUrl}"]`
    );

    if (selectedFilter) {
        selectedFilter.click();
    }

}




async function toggleFavourite(button) {
    const dishId = button.dataset.dishId;

    const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    try {
        const response = await fetch(`/favourite/${dishId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken || '',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.redirected) {
            window.location.href = response.url;
            return;
        }

        if (!response.ok) {
            alert('Could not update favourites. Please try again.');
            return;
        }

        const data = await response.json();

        button.classList.toggle('is-favourite', data.is_favourite);
        button.innerHTML = data.is_favourite ? '♥' : '♡';

        button.setAttribute(
            'aria-label',
            data.is_favourite ? 'Remove from favourites' : 'Add to favourites'
        );

    } catch (error) {
        alert('Something went wrong. Please try again.');
    }
}