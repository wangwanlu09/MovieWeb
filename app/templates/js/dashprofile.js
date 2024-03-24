function validatePasswords() {
    var newPassword = document.getElementById("newPassword").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    var newPasswordError = document.getElementById("newPasswordError");
    var confirmPasswordError = document.getElementById("confirmPasswordError");

    
    newPasswordError.innerText = "";
    confirmPasswordError.innerText = "";

    if (newPassword.length < 8) {
        newPasswordError.innerText = "Password must be at least 8 characters.";
    }

    if (confirmPassword !== newPassword) {
        confirmPasswordError.innerText = "Passwords do not match. Please re-enter.";
    }

    
    if (newPasswordError.innerText !== "" || confirmPasswordError.innerText !== "") {
        return;
    }


    alert("Form submitted successfully!");
};

function clearForm() {
    document.getElementById("newPassword").value = "";
    document.getElementById("confirmPassword").value = "";
    document.getElementById("newPasswordError").innerText = "";
    document.getElementById("confirmPasswordError").innerText = "";
};
