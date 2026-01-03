# FridgeFeast 
## Overview 
FridgeFeast is a recipe discovery engine designed to bridge the gap between "what's in the fridge" and "what's for dinner." Unlike standard recipe sites, it uses an ingredient-first logic to find meals that minimize food waste.

## Tools
- HTML
- CSS
- Javascript
- Spoonacular Food API

## Architecture
- <ins>UI Layer (HTML/CSS)</ins>: Captures user input (ingredients) and provides a grid-based display for results.
- <ins>Controller Layer (JavaScript)</ins>: Event Handling: Listens for clicks on the "Discover" button.
- <ins>Data Orchestration</ins>: Formats the ingredient string for API compatibility.
- <ins>State Management</ins>: Manages the visibility of the instruction modal and temporary storage of fetched data.
- <ins>Service Layer (Spoonacular API)</ins>: Processes queries based on ingredient availability.
