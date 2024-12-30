function autocomplete(input, dataList) {
    let currentFocus;

    input.addEventListener("input", function () {
        let val = this.value;
        closeAllLists();
        if (!val) return false;

        currentFocus = -1;
        let listContainer = document.createElement("div");
        listContainer.setAttribute("id", this.id + "-autocomplete-list");
        listContainer.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(listContainer);

        dataList.forEach(function (item) {
            if (item.substr(0, val.length).toUpperCase() === val.toUpperCase()) {
                let listItem = document.createElement("div");
                listItem.innerHTML = `<strong>${item.substr(0, val.length)}</strong>${item.substr(val.length)}`;
                listItem.innerHTML += `<input type='hidden' value='${item}'>`;

                listItem.addEventListener("click", function () {
                    input.value = this.querySelector("input").value;
                    closeAllLists();
                });

                listContainer.appendChild(listItem);
            }
        });
    });

    input.addEventListener("keydown", function (e) {
        let listItems = document.getElementById(this.id + "-autocomplete-list");
        if (listItems) listItems = listItems.getElementsByTagName("div");

        if (e.keyCode === 40) {
            currentFocus++;
            addActive(listItems);
        } else if (e.keyCode === 38) {
            currentFocus--;
            addActive(listItems);
        } else if (e.keyCode === 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (listItems) listItems[currentFocus].click();
            }
        }
    });

    function addActive(listItems) {
        if (!listItems) return false;
        removeActive(listItems);
        if (currentFocus >= listItems.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = listItems.length - 1;
        listItems[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(listItems) {
        for (let item of listItems) {
            item.classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        let items = document.getElementsByClassName("autocomplete-items");
        for (let item of items) {
            if (elmnt !== item && elmnt !== input) {
                item.parentNode.removeChild(item);
            }
        }
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const departureInput = document.getElementById("departure_city");
    const destinationInput = document.getElementById("destination_city");

    const airportCodes = JSON.parse(document.getElementById("airport-data").textContent);

    autocomplete(departureInput, airportCodes);
    autocomplete(destinationInput, airportCodes);
});
