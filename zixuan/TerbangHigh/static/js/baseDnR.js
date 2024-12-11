
 // Function to toggle the visibility of the meal sections
function toggleBaggageModification() {
var baggageSection = document.getElementById('baggageSection');

// Toggle the display of both sections when the button is clicked
if (baggageSection.style.display === "none") {
    baggageSection.style.display = "block";
} else {
    baggageSection.style.display = "none";
    }
}

// Function to handle baggage selection
function toggleSelection(element, weight, price) {

// Remove 'selected' class from all boxes
const allBoxes = document.querySelectorAll('.baggage-box');
allBoxes.forEach(box => box.classList.remove('selected'));

// Add 'selected' class to clicked box
element.classList.add('selected');

// Optional: You can store the baggage weight and price in hidden fields or session data
console.log(`Selected baggage: ${weight}, Price: MYR ${price}`);
}

// Function to toggle the visibility of the meal sections
function toggleMealOption() {
var mealSection = document.getElementById('mealSection');

// Toggle the display of both sections when the button is clicked
if (mealSection.style.display === "none") {
    mealSection.style.display = "block";
} else {
    mealSection.style.display = "none";
    }
}
            
function updateQuantity(mealId, change) {
var mealElement = document.getElementById(mealId);
var currentQuantity = parseInt(mealElement.textContent);
currentQuantity += change;

// Limit the quantity to a maximum of 3
if (currentQuantity > 3) currentQuantity = 3;
            
// Update quantity
if (currentQuantity < 0) currentQuantity = 0;
mealElement.textContent = currentQuantity;

// Enable or disable buttons
document.getElementById("decrease_" + mealId.split('_')[1]).disabled = currentQuantity === 0;
document.getElementById("increase_" + mealId.split('_')[1]).disabled = currentQuantity === 3;
}

// Function to show the tooltip
function showTooltip(tooltipId) {
    document.getElementById(tooltipId).style.display = "block";
}

// Function to hide the tooltip
function hideTooltip(tooltipId) {
    document.getElementById(tooltipId).style.display = "none";
}

// Function to toggle the visibility of the special assistance sections
function toggleSpecialAssistance() {
var wheelchairSection = document.getElementById('wheelchairSection');
var umnrSection = document.getElementById('umnrSection');

// Toggle the display of both sections when the button is clicked
if (wheelchairSection.style.display === "none") {
    wheelchairSection.style.display = "block";
    umnrSection.style.display = "block";
} else {
    wheelchairSection.style.display = "none";
    umnrSection.style.display = "none";
    }
}

