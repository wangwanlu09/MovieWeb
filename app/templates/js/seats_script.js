const container = document.querySelector('.container');
const seats = document.querySelectorAll('.row .seat:not(.occupied)');
const count = document.getElementById('count');

let selectedSeats = [];

// Update total and count
function updateSelectedCount() {
    const selectedSeats = document.querySelectorAll('.row .seat.selected');

    // Map the selected seats to their labels (A1, B2, etc.)
    const seatsLabels = [...selectedSeats].map((seat) => seat.dataset.label);

    // Update the count span with the selected seats count
    const selectedSeatsCount = selectedSeats.length;
    count.innerText = selectedSeatsCount;

    // Display the selected seats information
    const selectedSeatsInfo = seatsLabels.join(', '); // Join seat labels with commas
    document.getElementById('selected-seats-info').innerText = selectedSeatsInfo;
}

// Seat click event
container.addEventListener('click', (e) => {
    if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
        e.target.classList.toggle('selected');
        updateSelectedCount();
    }
});

// Initial count
updateSelectedCount();

