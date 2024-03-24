
const container = document.querySelector('.container');
const seats = document.querySelectorAll('.row .seat:not(.occupied)');
const count = document.getElementById('count');

const maxSeatsAllowed = document.getElementById('data-total-count').value;
const total_price_numeric = document.getElementById('total_price_numeric').value;
const movieid = document.getElementById('movieid').value;
const sessionid = document.getElementById('sessionid').value;
const cinemaid = document.getElementById('cinemaid').value;
const promotionid = document.getElementById('promotionid').value;
const ticket_quantities_dict = document.getElementById('ticket_quantities_dict').value;



let selectedSeats = [];
let seatSelectedcount = 0;

function updateSelectedCount() {
    const selectedSeats = document.querySelectorAll('.row .seat.selected');
    
    // Map the selected seats to their labels (A1, B2, etc.)
    const seatsLabels = [...selectedSeats].map((seat) => seat.dataset.label);
    
    const seatsValue = [...selectedSeats].map((seat) => seat.dataset.value);
    // Update the count span with the selected seats count
    const selectedSeatsCount = selectedSeats.length;
   
    count.innerText = selectedSeatsCount;

    // Display the selected seats information
    const selectedSeatsInfo = seatsLabels.join(', '); // Join seat labels with commas
    document.getElementById('selected-seats-info').innerText = selectedSeatsInfo;
    return seatsValue;
}

function updateSelectedSeats() {
    selectedSeats = [...document.querySelectorAll('.row .seat.selected')];
    seatSelectedcount = selectedSeats.length;
    if (seatSelectedcount > maxSeatsAllowed) {
        // Disable click event on all seats
        seats.forEach(seat => seat.removeEventListener('click', handleSeatClick));
        updateSelectedCount();
    }else{
         // Enable click event on all seats
         seats.forEach(seat => seat.addEventListener('click', handleSeatClick));
         updateSelectedCount();
    }
}
function sendSestidtoBackendAndRedirect() {
    var seatsValue = updateSelectedCount();

    if (!seatsValue || seatsValue.length === 0) {
        alert("Number of seats selected is less than the number of tickets! ")
        return; // Stop further processing
    }

    // Check if seatsValue is smaller than maxSeatsAllowed
    if (seatsValue.length < maxSeatsAllowed) {
        alert("Number of seats selected is less than the number of tickets! ")
        return; // Stop further processing
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/add_seats", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // var dataToSend = { seatsValue: seatsValue };
    var dataToSend = { seatsValue: seatsValue,promotionid:promotionid, sessionid : sessionid, ticket_quantities_dict : ticket_quantities_dict, total_price_numeric : total_price_numeric };
    xhr.onreadystatechange = function() {
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
          window.location.href = '/payment/booking';
        }
    }
    xhr.send(JSON.stringify((dataToSend)));
    
    
}


function handleSeatClick(e) {
    if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
     
        if (selectedSeats.length < maxSeatsAllowed || e.target.classList.contains('selected')) {
            // Toggle the 'selected' class
            e.target.classList.toggle('selected');
            // Update the selected seats and count
            updateSelectedSeats();
        } else {
            // Display a message or take some action to indicate that the maximum seats have been reached
            alert("Maximum seats reached. You cannot select more seats.");
        }
    }
}

// Add click event listener to seats during initialization
seats.forEach(seat => seat.addEventListener('click', handleSeatClick));

// Initialize seat count
updateSelectedSeats();

