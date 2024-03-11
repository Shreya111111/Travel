document.getElementById("create-tour-btn").addEventListener("click", function() {
    // Collect form data
    var destination = document.getElementById("destination").value;
    var duration = document.getElementById("duration").value;
    var activities = document.getElementById("activities").value;
    var accommodations = document.getElementById("accommodations").value;
    var transportation = document.getElementById("transportation").value;
    
    // Example: You would integrate with Razorpay here to handle payment processing
    
    // For demonstration purposes, alert the collected data
    var tourDetails = "Destination: " + destination + "\n" +
                      "Duration: " + duration + " days\n" +
                      "Activities: " + activities + "\n" +
                      "Accommodations: " + accommodations + "\n" +
                      "Transportation: " + transportation;
    alert("Your custom tour details:\n\n" + tourDetails);
});
