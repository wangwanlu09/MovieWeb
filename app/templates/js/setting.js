function validateContact() {
    var newphoneNumber = document.getElementById("phoneNumber").value;
    var newemailCinema = document.getElementById("emailCinema").value;
    var newaddressCinema = document.getElementById("addressCinema").value;


    var newphoneNumberError = document.getElementById("newphoneNumberError");
    var newemailCinemaError = document.getElementById("newemailCinemaError");
    var newaddressCinemaError = document.getElementById("newaddressCinemaError");


    if (newphoneNumber.length < 11) {
        newphoneNumberError.innerText = "Phone number must be at least 11 characters.";
    } else {
        newphoneNumberError.innerText = "";
    }

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(newemailCinema)) {
        newemailCinemaError.innerText = "Please enter a valid email address.";
    } else {
        newemailCinemaError.innerText = "";
    }

    if (newaddressCinema.length === 0) {
        newaddressCinemaError.innerText = "Address is required.";
    } else {
        newaddressCinemaError.innerText = "";
    }

    if (newphoneNumberError.innerText !== "" || newemailCinemaError.innerText !== "" || newaddressCinemaError.innerText !== "") {
        return;
    }

    var form = document.getElementById("editContact"); 
    form.submit();
};
    
    function clearForm() {
    document.getElementById("phoneNumber").value = "";
    document.getElementById("emailCinema").value = "";
    document.getElementById("addressCinema").value = "";
    document.getElementById("phoneNumber").innerText = "";
    document.getElementById("emailCinema").innerText = "";
    document.getElementById("addressCinema").innerText = "";
};