
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
function selectBaggage(element, weight, price) {

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
            
function toggleCartSelection(icon) {
    // Deselect all other icons
    const allIcons = document.querySelectorAll('.checked-icon');
    allIcons.forEach(function(item) {
      if (item !== icon) {
        item.classList.remove('selected');
      }
    });

    // Toggle the clicked icon
    icon.classList.toggle('selected');
  
// Function to show the tooltip
function showTooltip(tooltipId) {
    document.getElementById(tooltipId).style.display = "block";
}
}

// Function to hide the tooltip
function hideTooltip(tooltipId) {
    document.getElementById(tooltipId).style.display = "none";
}

// Function to toggle the visibility of the special assistance sections
 function toggleSpecialAssistance() {
            var wheelchairSection = document.getElementById('wheelchairSection');
            var umnrSection = document.getElementById('umnrSection');
            if (wheelchairSection.style.display === 'none') {
                wheelchairSection.style.display = 'block';
                umnrSection.style.display = 'block';
            } else {
                wheelchairSection.style.display = 'none';
                umnrSection.style.display = 'none';
            }
        }

        function toggleDropdown(dropdownId) {
            var dropdownContent = document.getElementById(dropdownId);
            if (dropdownContent.style.display === 'block') {
                dropdownContent.style.display = 'none';
            } else {
                dropdownContent.style.display = 'block';
            }
        }

        function selectOption(buttonId, optionText, dropdownId) {
            var button = document.getElementById(buttonId);
            button.textContent = optionText;
            var dropdownContent = document.getElementById(dropdownId);
            dropdownContent.style.display = 'none';
        }

