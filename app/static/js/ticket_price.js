    // Assuming tickets is a global variable containing the ticket data
    var tickets = {{ tickets | tojson | safe }};

    function calculateTotal() {
        var totalPrice = 0;

        // Loop through each ticket type
        tickets.forEach(function(ticket) {
            // Get the selected quantity for each ticket type
            var count = parseInt(document.getElementById(ticket.ticket_type + "Count").value);

            // Calculate the subtotal for each ticket type
            var subtotal = count * ticket.price;

            // Add the subtotal to the total price
            totalPrice += subtotal;
        });

        // Update the display of the total price element
        document.getElementById("totalPrice").innerText = "$" + totalPrice.toFixed(2);
        
        // Return the calculated total price
        return totalPrice;
    }

    function sendTotalPriceToBackendAndNavigate() {
        // Call calculateTotal to get the totalPrice
        var totalPrice = calculateTotal();
        
        var totalPriceString = totalPrice !== undefined ? totalPrice.toString() : '0';

        // Log the calculated total price
        console.log("Total price calculated:", totalPriceString);

        // Log the data being sent to the backend
        console.log("Sending data to backend:", { totalPrice: totalPriceString });

        // Add additional logic here to send the total price to the backend
        // For example, you can trigger a form submission or an AJAX request
        // This is just a placeholder function, you may need to modify it based on your backend communication requirements

        // Send the total price to the Flask backend (you can use Ajax or other methods to send the request)
        // The following is a simplified example
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/total_price", true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        var dataToSend = { totalPrice: totalPriceString };
        xhr.send(JSON.stringify(dataToSend));
        
        window.location.href = "{{ url_for('booking.select_seats') }}";
    }