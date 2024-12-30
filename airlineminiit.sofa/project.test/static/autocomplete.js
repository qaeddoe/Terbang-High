function setupAutocomplete(fromId, toId, airports) {
    function attachAutocomplete(inputId, modalId, airportList) {
        const input = document.getElementById(inputId);
        const modal = document.getElementById(modalId);
        const suggestionsContainer = document.getElementById("suggestions");
        const searchBox = document.getElementById("modal-search");
        const modalTitle = document.getElementById("modal-title");

        // Open modal on focus
        input.addEventListener("focus", () => {
            modal.style.display = "flex";
            modalTitle.textContent = inputId === fromId ? "Select Origin" : "Select Destination";
            searchBox.value = "";
            suggestionsContainer.innerHTML = "";
            searchBox.focus();

            // Keep track of the current input
            searchBox.setAttribute("data-target", inputId);
        });

        // Close modal
        document.getElementById("close-modal").addEventListener("click", () => {
            modal.style.display = "none";
        });

        // Filter suggestions based on user input (starts with matching)
        searchBox.addEventListener("input", () => {
            const query = searchBox.value.toLowerCase();
            suggestionsContainer.innerHTML = ""; // Clear previous suggestions

            const matches = airportList.filter(airport =>
                airport.name.toLowerCase().startsWith(query) || airport.code.toLowerCase().startsWith(query)
            );

            matches.forEach(match => {
                const suggestionItem = document.createElement("div");
                suggestionItem.classList.add("suggestion-item");
                suggestionItem.innerHTML = `
                    <span class="airport-name">${match.name}</span>
                    <span class="airport-code">${match.code}</span>
                    <span class="airport-info">${match.airport}</span>
                `;

                // Floating info box when hovered
                suggestionItem.addEventListener("mouseenter", () => {
                    const floatingBox = document.createElement("div");
                    floatingBox.classList.add("floating-box");
                    floatingBox.innerHTML = `
                        <strong>${match.name}</strong><br>
                        <em>${match.airport}</em><br>
                        Code: ${match.code}
                    `;
                    suggestionItem.appendChild(floatingBox);
                });

                suggestionItem.addEventListener("mouseleave", () => {
                    const floatingBox = suggestionItem.querySelector('.floating-box');
                    if (floatingBox) {
                        floatingBox.remove();
                    }
                });

                suggestionItem.addEventListener("click", () => {
                    const targetInput = searchBox.getAttribute("data-target");
                    document.getElementById(targetInput).value = `${match.name} (${match.code})`;
                    modal.style.display = "none";
                });

                suggestionsContainer.appendChild(suggestionItem);
            });

            if (matches.length === 0) {
                const noResults = document.createElement("div");
                noResults.classList.add("no-results");
                noResults.textContent = "No matching airports found.";
                suggestionsContainer.appendChild(noResults);
            }
        });
    }

    // Modal for passenger count and cabin class
    document.getElementById("passenger-cabin-box").addEventListener("click", () => {
        document.getElementById("passenger-cabin-modal").style.display = "flex";
    });

    document.getElementById("close-passenger-cabin-modal").addEventListener("click", () => {
        document.getElementById("passenger-cabin-modal").style.display = "none";

        // Update display text
        const adults = parseInt(document.getElementById("adults-count").textContent);
        const children = parseInt(document.getElementById("children-count").textContent);
        const infants = parseInt(document.getElementById("infants-count").textContent);
        const selectedClass = document.querySelector(".cabin-option.active").dataset.class;

        const totalPassengers = adults + children + infants;
        document.getElementById("passenger-cabin-display").value = `${totalPassengers} Passengers, ${selectedClass}`;
    });

    // Handle increment and decrement buttons
    const maxPassengers = 5;
    document.querySelectorAll(".increment, .decrement").forEach(button => {
        button.addEventListener("click", () => {
            const type = button.dataset.type;
            const countElement = document.getElementById(`${type}-count`);
            let count = parseInt(countElement.textContent);

            if (button.classList.contains("increment") && getTotalPassengers() < maxPassengers) {
                count++;
            } else if (button.classList.contains("decrement") && count > 0) {
                count--;
            }

            countElement.textContent = count;
        });
    });

    // Update cabin class selection
    document.querySelectorAll(".cabin-option").forEach(button => {
        button.addEventListener("click", () => {
            document.querySelectorAll(".cabin-option").forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");
        });
    });

    // Calculate total passengers
    function getTotalPassengers() {
        const adults = parseInt(document.getElementById("adults-count").textContent);
        const children = parseInt(document.getElementById("children-count").textContent);
        const infants = parseInt(document.getElementById("infants-count").textContent);
        return adults + children + infants;
    }

    // Attach autocomplete to both "From" and "To" inputs
    attachAutocomplete(fromId, "airport-modal", airports);
    attachAutocomplete(toId, "airport-modal", airports);
}
