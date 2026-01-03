
const API_KEY = 'e213dcb05b2e49d995452337413ad068';
const searchBtn = document.getElementById('searchBtn');
const recipeGrid = document.getElementById('recipeGrid');
const modal = document.getElementById('recipeModal');
const modalBody = document.getElementById('modalBody');
const closeBtn = document.querySelector('.close');

searchBtn.addEventListener('click', getRecipes);
closeBtn.onclick = () => modal.style.display = "none";
window.onclick = (event) => { if (event.target == modal) modal.style.display = "none"; };

async function getRecipes() {
    const ingredients = document.getElementById('ingredientInput').value;
    if (!ingredients) return alert("Please enter some ingredients first!");

    recipeGrid.innerHTML = "<p>Searching...</p>";

    try {
        const response = await fetch(`https://api.spoonacular.com/recipes/findByIngredients?ingredients=${ingredients}&number=12&apiKey=${API_KEY}`);
        const data = await response.json();
        renderCards(data);
    } catch (err) {
        recipeGrid.innerHTML = "<p>Error: Could not fetch recipes.</p>";
    }
}

function renderCards(recipes) {
    recipeGrid.innerHTML = recipes.map(recipe => `
        <div class="recipe-card" onclick="getInstructions(${recipe.id})">
            <img src="${recipe.image}" alt="${recipe.title}">
            <div style="padding:15px;">
                <h4 style="margin:0;">${recipe.title}</h4>
            </div>
        </div>
    `).join('');
}

async function getInstructions(id) {
    modal.style.display = "block";
    modalBody.innerHTML = "Fetching instructions...";

    try {
        const response = await fetch(`https://api.spoonacular.com/recipes/${id}/information?apiKey=${API_KEY}`);
        const recipe = await response.json();
        
        modalBody.innerHTML = `
            <h2>${recipe.title}</h2>
            <img src="${recipe.image}" style="width:100%; border-radius:10px;">
            <h3>Ingredients needed:</h3>
            <ul>${recipe.extendedIngredients.map(i => `<li>${i.original}</li>`).join('')}</ul>
            <h3>Instructions:</h3>
            <div>${recipe.instructions || "Click 'View Original' for steps."}</div>
            <br>
            <a href="${recipe.sourceUrl}" target="_blank">View Original Recipe</a>
        `;
    } catch (err) {
        modalBody.innerHTML = "Failed to load details.";
    }
}

function renderCards(recipes) {
    recipeGrid.innerHTML = recipes.map((recipe, index) => `
        <div class="recipe-card" 
             style="animation: fadeIn 0.5s ease forwards ${index * 0.1}s; opacity: 0;"
             onclick="getInstructions(${recipe.id})">
            <img src="${recipe.image}" alt="${recipe.title}">
            <div class="recipe-info">
                <h3 style="margin:0; font-size: 1.1rem;">${recipe.title}</h3>
                <p style="color: var(--primary); font-size: 0.9rem; margin-top: 10px;">
                    View Details →
                </p>
            </div>
        </div>
    `).join('');
}
