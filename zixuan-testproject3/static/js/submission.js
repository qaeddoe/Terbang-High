function sumbitBaggage() {
  var userId = sessionStorage.getItem("selectedUser");
  console.log(userId);
  var D_baggage = document.getElementById("selected-baggage-load").innerHTML;
  var R_baggage = document.getElementById(
    "selected-baggage-load-return"
  ).innerHTML;
  var baggage = [D_baggage, R_baggage];
  sessionStorage.setItem("baggage", JSON.stringify(baggage));
  console.log(baggage);

  fetch("/submit/preference", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      type: "baggage",
      data: baggage,
      userId: userId,
    }),
  });
}

function submitAssistance() {
  let userId = sessionStorage.getItem("selectedUser");
  console.log(userId);
  var D_selectedAssistance = document.getElementById(
    "selected-assistance-request"
  ).textContent;
  var R_selectedAssistance = document.getElementById(
    "selected-assistance-request-return"
  ).textContent;
  console.log(D_selectedAssistance);
  console.log(R_selectedAssistance);

  var assistance = [D_selectedAssistance, R_selectedAssistance];
  sessionStorage.setItem("assistance", JSON.stringify(assistance));

  fetch("/submit/preference", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      type: "assistance",
      data: assistance,
      userId: userId,
    }),
  });
}

function submitMeal() {
  let userId = sessionStorage.getItem("selectedUser");
  console.log(userId);
  var D_meal = document.getElementById("selected-meal-set").innerHTML;
  var R_meal = document.getElementById("selected-meal-set-return").innerHTML;
  var meal = [D_meal, R_meal];
  sessionStorage.setItem("meal", JSON.stringify(meal));
  console.log(meal);

  fetch("/submit/preference", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      type: "meal",
      data: meal,
      userId: userId,
    }),
  });
}



function submitSeat() {
  var D_selectedSeat = document.getElementById("selected-seat-id").textContent;
  var R_selectedSeat = document.getElementById(
    "selected-seat-id-return"
  ).textContent;

  var allD_seat = document.querySelectorAll(".seat");
  var allR_seat = document.querySelectorAll(".Rseat");

  if (D_selectedSeat == "None") {
    var number = Math.floor(Math.random() * allD_seat.length);
    D_selectedSeat = allD_seat[number].id;
  }

  if (R_selectedSeat == "None") {
    var number = Math.floor(Math.random() * allR_seat.length);
    R_selectedSeat = allR_seat[number].id;
  }

  var seat = [D_selectedSeat, R_selectedSeat];
  sessionStorage.setItem("seat", JSON.stringify(seat));
  console.log(seat);

  let userId = sessionStorage.getItem("selectedUser");
  console.log(userId);

  fetch("/submit/preference", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      type: "seat",
      data: seat,
      userId: userId,
    }),
  });
}

// -----------------  End of submission.js -----------------

document.addEventListener("DOMContentLoaded", function () {
  // Function to handle seat selection (both outbound and return)
  function handleSeatSelection(seatClass, seatIdElement) {
    document.querySelectorAll(seatClass).forEach((seat) => {
      seat.addEventListener("click", (event) => {
        console.log("Seat ID: " + seat.id);
        // Prevent the event from bubbling up to the parent elements
        event.stopPropagation();

        // Deselect all seats
        document
          .querySelectorAll(seatClass)
          .forEach((s) => s.classList.remove("selected"));

        // Select clicked seat
        seat.classList.add("selected");

        // Display selected seat ID
        document.getElementById(seatIdElement).textContent = seat.id;
      });

      seat.addEventListener("dblclick", () => {
        seat.classList.remove("selected");
        document.getElementById(seatIdElement).textContent = "None";
      });
    });
  }

  // Handle seat selection for both outbound and return seats

  handleSeatSelection(".seat", "selected-seat-id");
  handleSeatSelection(".Rseat", "selected-seat-id-return");
});

// Function to show return seats popup
function showReturnSeatsPopup() {
  document.getElementById("seats-section").style.display = "none"; // Hide baggage section
  document.getElementById("return-seats-popup").style.display = "block"; // Show return flight popup
}

// Function to hide return seats popup
function hideReturnSeatsPopup() {
  document.getElementById("seats-section").style.display = "block"; // Show baggage section
  document.getElementById("return-seats-popup").style.display = "none"; // Hide return flight popup
}
