const airports = [
    { name: 'Kuala Lumpur International Airport (KLIA)', code: 'KUL', state: 'Selangor' },
    { name: 'Sultan Abdul Aziz Shah Airport (Subang)', code: 'WMKQ', state: 'Selangor' },
    { name: 'Penang International Airport', code: 'PEN', state: 'Penang' },
    { name: 'Langkawi International Airport', code: 'LGK', state: 'Kedah' },
    { name: 'Kota Kinabalu International Airport', code: 'BKI', state: 'Sabah' },
    { name: 'Johor Bahru International Airport', code: 'JHB', state: 'Johor' },
    { name: 'Kuching International Airport', code: 'KCH', state: 'Sarawak' },
    { name: 'Kuala Terengganu Sultan Mahmud Airport', code: 'TGG', state: 'Terengganu' },
    { name: 'Malacca International Airport', code: 'MKZ', state: 'Melaka' },
    { name: 'Alor Setar International Airport', code: 'AOR', state: 'Kedah' },
    { name: 'Ipoh Airport', code: 'IPH', state: 'Perak' },
    { name: 'Sibu Airport', code: 'SBW', state: 'Sarawak' },
    { name: 'Bintulu Airport', code: 'BTU', state: 'Sarawak' },
    { name: 'Miri Airport', code: 'MYY', state: 'Sarawak' },
    { name: 'Sandakan Airport', code: 'SDK', state: 'Sabah' }
];

// Autocomplete function
function autocomplete(input) {
    let currentFocus;

    input.addEventListener("input", function () {
        const val = this.value;
        closeAllLists();
        if (!val) return false;
        currentFocus = -1;

        const list = document.createElement("DIV");
        list.setAttribute("id", `${this.id}-autocomplete-list`);
        list.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(list);

        airports.forEach((airport) => {
            if (
                airport.name.toLowerCase().startsWith(val.toLowerCase()) ||
                airport.code.toLowerCase().startsWith(val.toLowerCase()) ||
                airport.state.toLowerCase().startsWith(val.toLowerCase())
            ) {
                const item = document.createElement("DIV");
                item.innerHTML = `
                    <div class="suggestion-content">
                        <span>${airport.name} - ${airport.state}</span>
                        <span class="autocomplete-code">${airport.code}</span>
                    </div>`;
                item.addEventListener("click", function () {
                    input.value = `${airport.name} (${airport.code})`;
                    closeAllLists();
                });
                list.appendChild(item);
            }
        });
    });

    input.addEventListener("keydown", function (e) {
        let list = document.getElementById(`${this.id}-autocomplete-list`);
        if (list) list = list.getElementsByTagName("div");
        if (e.key === "ArrowDown") {
            currentFocus++;
            addActive(list);
        } else if (e.key === "ArrowUp") {
            currentFocus--;
            addActive(list);
        } else if (e.key === "Enter") {
            e.preventDefault();
            if (currentFocus > -1) {
                if (list) list[currentFocus].click();
            }
        }
    });

    function addActive(list) {
        if (!list) return false;
        removeActive(list);
        if (currentFocus >= list.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = list.length - 1;
        list[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(list) {
        Array.from(list).forEach((item) => item.classList.remove("autocomplete-active"));
    }
}

// Close all autocomplete lists
function closeAllLists(el) {
    const items = document.getElementsByClassName("autocomplete-items");
    Array.from(items).forEach((item) => {
        if (el !== item && el !== item.parentNode) {
            item.parentNode.removeChild(item);
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    // Initialize autocomplete for both input fields
    autocomplete(document.getElementById("departure_city"));
    autocomplete(document.getElementById("destination_city"));

    // Swap button functionality
    const switchButton = document.getElementById("switch_button");
    switchButton.addEventListener("click", () => {
        const departureInput = document.getElementById("departure_city");
        const destinationInput = document.getElementById("destination_city");
        const tempValue = departureInput.value;
        departureInput.value = destinationInput.value;
        destinationInput.value = tempValue;
    });

    // Dynamic date field handling
    const flightTypeField = document.getElementById("flight_type");
    const arrivalDateContainer = document.getElementById("arrival_date_container");
    flightTypeField.addEventListener("change", () => {
        if (flightTypeField.value === "returning") {
            arrivalDateContainer.style.display = "block";
            document.getElementById("arrival_date").required = true;
        } else {
            arrivalDateContainer.style.display = "none";
            document.getElementById("arrival_date").required = false;
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, "0");
    const dd = String(today.getDate()).padStart(2, "0");
    const minDate = `${yyyy}-${mm}-${dd}`;

    // Set the min attribute for the departure date
    const departureDateInput = document.getElementById("departure_date");
    if (departureDateInput) {
        departureDateInput.setAttribute("min", minDate);
    }

    // Set the min attribute for the arrival date
    const arrivalDateInput = document.getElementById("arrival_date");
    if (arrivalDateInput) {
        arrivalDateInput.setAttribute("min", minDate);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const passengersCabinInput = document.getElementById("passengers_cabin");
    const passengerPopup = document.getElementById("passenger_popup");
    const applyChangesButton = document.getElementById("apply_changes");

    let passengers = { adults: 1, children: 0, infants: 0 };
    const maxPassengers = 5;

    // Open Popup
    passengersCabinInput.addEventListener("click", () => {
        passengerPopup.style.display = "block";
    });

    // Close Popup when clicking outside
    document.addEventListener("click", (e) => {
        if (!passengerPopup.contains(e.target) && e.target !== passengersCabinInput) {
            passengerPopup.style.display = "none";
        }
    });

    // Counter functionality
    document.querySelectorAll(".increment, .decrement").forEach((button) => {
        button.addEventListener("click", () => {
            const target = button.getAttribute("data-target");
            const isIncrement = button.classList.contains("increment");
            let newCount = passengers[target] + (isIncrement ? 1 : -1);

            // Validate limits
            const totalPassengers =
                passengers.adults + passengers.children + passengers.infants;
            if (newCount < 0 || (isIncrement && totalPassengers >= maxPassengers)) {
                return;
            }

            passengers[target] = newCount;
            document.getElementById(`${target}-count`).innerText = newCount;
        });
    });

    // Apply Changes
    document.getElementById("apply_changes").addEventListener("click", () => {
        const adults = parseInt(document.getElementById("adults-count").textContent, 10);
        const children = parseInt(document.getElementById("children-count").textContent, 10);
        const infants = parseInt(document.getElementById("infants-count").textContent, 10);
    
        const totalPassengers = adults + children + infants;
    
        // Update the hidden input field
        document.getElementById("passengers").value = totalPassengers;
    
        // Update the display in the input field
        document.getElementById("passengers_cabin").value = `${totalPassengers} Passenger${totalPassengers > 1 ? "s" : ""}`;
    
        // Close the popup box and overlay
        const passengerPopup = document.getElementById("passenger_popup");
        const overlay = document.getElementById("overlay");
    
        passengerPopup.style.display = "none";
        overlay.style.display = "none";
    });
    
    
});

document.addEventListener("DOMContentLoaded", () => {
    const passengersCabinInput = document.getElementById("passengers_cabin");
    const passengerPopup = document.getElementById("passenger_popup");
    const overlay = document.getElementById("overlay");
    const applyChangesButton = document.getElementById("apply_changes");

    let passengers = { adults: 1, children: 0, infants: 0 };
    const maxPassengers = 5;

    // Open Popup
    passengersCabinInput.addEventListener("click", () => {
        passengerPopup.style.display = "block";
        overlay.style.display = "block";
    });

    // Close Popup when clicking outside
    overlay.addEventListener("click", () => {
        passengerPopup.style.display = "none";
        overlay.style.display = "none";
    });

    // Counter functionality
    document.querySelectorAll(".increment, .decrement").forEach((button) => {
        button.addEventListener("click", () => {
            const target = button.getAttribute("data-target");
            const isIncrement = button.classList.contains("increment");
            let newCount = passengers[target] + (isIncrement ? 1 : -1);

            // Validate limits
            const totalPassengers =
                passengers.adults + passengers.children + passengers.infants;
            if (newCount < 0 || (isIncrement && totalPassengers >= maxPassengers)) {
                return;
            }

            passengers[target] = newCount;
            document.getElementById(`${target}-count`).innerText = newCount;
        });
    });

    // Apply Changes
    applyChangesButton.addEventListener("click", () => {
        const cabinClass = document.getElementById("cabin_class").value;
        const totalPassengers =
            passengers.adults + passengers.children + passengers.infants;

        passengersCabinInput.value = `${totalPassengers} Passenger${
            totalPassengers > 1 ? "s" : ""
        }, ${cabinClass}`;
        passengerPopup.style.display = "none";
        overlay.style.display = "none";
    });
});
