const regions = {

    north: {
        image: "north icon.png",
        name: "NORTH INDIA",
        title: "The Royal",
        span: "North",
        story: "From royal kitchens and ancient trade routes to bustling streets and family tables, the food of North India carries generations of stories.",
        knownFor: "rich gravies, wheat-based flatbreads, and heavy use of dairy products"
    },

    south: {
        image: "south icon.png",
        name: "SOUTH INDIA",
        title: "The Tropical",
        span: "South",
        story: "From temple kitchens to coastal homes, South Indian food brings together rice, spices, coconut and traditions passed down through generations.",
        knownFor: "rice-based dishes, coconut, spices, fermented foods, and coastal flavours"
    },

    east: {
        image: "east icon.png",
        name: "EAST INDIA",
        title: "The Eastern",
        span: "East",
        story: "Eastern India carries a beautiful blend of river, coast and fertile land, creating a cuisine rich with delicate flavours and age-old traditions.",
        knownFor: "heavy use of rice, freshwater fish, distinct mustard flavors, and world-famous dairy-based sweets"
    },

    west: {
        image: "west icon.png",
        name: "WEST INDIA",
        title: "The Colourful",
        span: "West",
        story: "From vibrant street food to royal kitchens and coastal traditions, Western India is a celebration of bold flavours, textures and colour.",
        knownFor: "vibrant diversity, blending sweet-and-salty vegetarian dishes in Gujarat, bold street food and coastal flavors in Maharashtra, and Portuguese-infused seafood in Goa."
    }
};


const tabs = document.querySelectorAll(".region-tab");

const regionImage = document.getElementById("regionImage");
const pageRegion = document.getElementById("pageRegion");
const regionTitle = document.getElementById("regionTitle");
const regionStory = document.getElementById("regionStory");
const regionKnownFor = document.getElementById("regionKnownFor");
const exploreRegion = document.getElementById("exploreRegion");

const pages = document.querySelectorAll(".book-page");


function showRegion(regionName) {

    const region = regions[regionName];

    if (!region) {
        return;
    }

    // Tiny animation
    pages.forEach(page => {
        page.classList.add("changing");
    });


    regionImage.src = `/static/images/${region.image}`;

    regionImage.alt = region.name;

    pageRegion.textContent = region.name;

    regionTitle.innerHTML =
        `${region.title}<br><span>${region.span}</span>`;

    regionStory.textContent = region.story;

    regionKnownFor.textContent = region.knownFor;

    exploreRegion.innerHTML =
        `EXPLORE ${regionName.toUpperCase()} <span>→</span>`;


    tabs.forEach(tab => {
        tab.classList.remove("active");
    });

    const activeTab = document.querySelector(
        `.region-tab[data-region="${regionName}"]`
    );

    if (activeTab) {
        activeTab.classList.add("active");
    }


    // Remove tiny animation
    setTimeout(() => {
        pages.forEach(page => {
            page.classList.remove("changing");
        });
    }, 200);
}


tabs.forEach(tab => {

    tab.addEventListener("click", function () {

        const selectedRegion = this.dataset.region;

        currentRegionIndex =
            regionOrder.indexOf(selectedRegion);

        showRegion(selectedRegion);

    });

});


exploreRegion.addEventListener("click", function () {

    const currentRegion =
        document.querySelector(".region-tab.active").dataset.region;

    const allDishesUrl = this.dataset.url;

    window.location.href =
        `${allDishesUrl}?region=${currentRegion}`;

});


let currentRegionIndex = 0;

const regionOrder = [
    "north",
    "south",
    "east",
    "west"
];

const regionFromHash = window.location.hash.replace("#", "");

if (regionFromHash && regions[regionFromHash]) {
    currentRegionIndex = regionOrder.indexOf(regionFromHash);
    showRegion(regionFromHash);
}


function previousDish() {

    currentRegionIndex--;

    if (currentRegionIndex < 0) {
        currentRegionIndex =
            regionOrder.length - 1;
    }

    showRegion(
        regionOrder[currentRegionIndex]
    );
}


function nextDish() {

    currentRegionIndex++;

    if (currentRegionIndex >= regionOrder.length) {
        currentRegionIndex = 0;
    }

    showRegion(
        regionOrder[currentRegionIndex]
    );
}

