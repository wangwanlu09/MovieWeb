

  /////when promotionid == 0,there will be no discount and will calculate total orignal price
  function calculateTotal() {
    var totalPrice = 0;
    var totalCount = 0;
    var ticketQuantities = {}; // Object to store ticketid and corresponding quantities

    // Loop through each ticket type
    tickets.forEach(function (ticket) {
      // Get the selected quantity for each ticket type
      var idNum = parseInt(document.getElementById(ticket.ticketid + "Count"));
      var count = parseInt(document.getElementById(ticket.ticketid + "Count").value);

      // Calculate the subtotal for each ticket type
      var subtotal = count * ticket.price;

      // Add the subtotal to the total price
      totalPrice += subtotal;
      totalCount += count;
      // Store ticketid and corresponding quantity in the object
      ticketQuantities[ticket.ticketid] = count;
    });
 
    // Update the display of the total price element
    document.getElementById("totalPrice").innerText = "$" + totalPrice.toFixed(2);

    // Set the values of the hidden input fields
    document.getElementById("hiddenTotalPrice").value = totalPrice.toFixed(2);
    document.getElementById("hiddenTotalCount").value = totalCount;
    document.getElementById("ticketQuantitiesHiddenInput").value = JSON.stringify(ticketQuantities);
 
    // Return the calculated values
    return { totalPrice, totalCount, ticketQuantities };
  }


    function sendDateToBackendAndNavigate() {
      // Call calculateTotal to update the hidden input fields
      var result = calculateTotal();

      // Check if totalPrice is 0
      if (result.totalPrice === 0) {
          // Do not submit the form
          return;
      }

      // Check if remaining seats are less than totalCount
      if (remaining_seats.no_of_seats < result.totalCount) {
          // Display a message to the user
          alert("Sorry, there are not enough available seats. Remaining seats: " + remaining_seats.no_of_seats);
          // Do not submit the form
          return;
      }

      // Submit the form
      document.getElementById("myFormId").submit();
  }
