const scrollRevealOption = {
  distance: "50px",
  origin: "bottom",
  duration: 1000,
};

// header container
ScrollReveal().reveal(".header__container h1", {
  ...scrollRevealOption,
});

ScrollReveal().reveal(".header__form", {
  ...scrollRevealOption,
  delay: 500,
});

// trending container
ScrollReveal().reveal(".trending__card", {
  ...scrollRevealOption,
  interval: 500,
});

// destination container
ScrollReveal().reveal(".destination__card", {
  duration: 1000,
  interval: 500,
});

// seller container
ScrollReveal().reveal(".seller__card", {
  ...scrollRevealOption,
  interval: 500,
});

// guide container
ScrollReveal().reveal(".guide__card", {
  ...scrollRevealOption,
  interval: 500,
});

//  client container
ScrollReveal().reveal(".client__card", {
  ...scrollRevealOption,
  interval: 500,
});
// main.js

// Define a variable to store the map
let map;

function initMap() {
  // Initialize the map (optional)
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });

  // Add a click event listener to the map
  map.addListener("click", function (event) {
    // Get the clicked location (latitude and longitude)
    const clickedLocation = event.latLng;

    // Reverse geocode the clicked location to get the address
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ location: clickedLocation }, function (results, status) {
      if (status === "OK") {
        // Get the formatted address
        const formattedAddress = results[0].formatted_address;

        // Update the destination input field with the formatted address
        document.getElementById("destination").value = formattedAddress;
      } else {
        console.error("Geocode failed: " + status);
      }
    });
  });
}

function searchOnMap() {
  // Get the user-entered destination
  const destination = document.getElementById("destination").value;

  // Use Geocoding to get the coordinates of the destination
  const geocoder = new google.maps.Geocoder();

  geocoder.geocode({ address: destination }, (results, status) => {
    if (status === "OK" && results[0]) {
      const location = results[0].geometry.location;

      // Pan to the location on the map
      map.panTo(location);

      // Add a marker for the destination
      new google.maps.Marker({
        position: location,
        map: map,
        title: destination,
      });
    } else {
      alert("Location not found");
    }
  });
}

// Example: Add event listener for a button with id 'checkAvailabilityBtn'
document.getElementById("checkAvailabilityBtn").addEventListener("click", function () {
  // Perform the desired action when the button is clicked
  console.log("Check Availability button clicked");
});
