
    function toggleDropdown(adultNumber) {
      const detailsBox = document.getElementById(`adult${adultNumber}Details`);
      const arrowIcon = document.getElementById(`arrow${adultNumber}`);

      if (detailsBox.style.display === "flex") {
        detailsBox.style.display = "none";
        arrowIcon.style.transform = "rotate(-45deg)"; // Arrow points down
      } else {
        detailsBox.style.display = "flex";
        arrowIcon.style.transform = "rotate(45deg)"; // Arrow points up
      }
    }

    // Show the popup based on type
    function showPopup(type) {
      if (type === 'departure') {
        document.getElementById('departureOverlay').style.display = 'flex';
      } else if (type === 'return') {
        document.getElementById('returnOverlay').style.display = 'flex';
      }
    }

    // Hide the popup based on type
    function hidePopup(type) {
      if (type === 'departure') {
        document.getElementById('departureOverlay').style.display = 'none';
      } else if (type === 'return') {
        document.getElementById('returnOverlay').style.display = 'none';
      }
    }


