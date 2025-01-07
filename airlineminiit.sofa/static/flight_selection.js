document.addEventListener("DOMContentLoaded", () => {
    const flightButtons = document.querySelectorAll(".select-flight-btn");
    const proceedButton = document.getElementById("proceed");

    let selectedFlightId = null;

    // Handle flight selection
    flightButtons.forEach((button) => {
        button.addEventListener("click", () => {
            // Highlight the selected flight and store its ID
            flightButtons.forEach((btn) => btn.classList.remove("selected"));
            button.classList.add("selected");
            selectedFlightId = button.getAttribute("data-flight-id");
        });
    });

    // Proceed to Payment
    proceedButton.addEventListener("click", () => {
        if (!selectedFlightId) {
            alert("Please select a flight before proceeding.");
            return;
        }

        // Redirect to payment page or send data via AJAX
        window.location.href = `/payment?flight_id=${selectedFlightId}`;
    });
});
