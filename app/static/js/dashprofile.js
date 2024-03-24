
function enableEditing(elementId) {
    var currentValue = document.getElementById(elementId).innerText.trim();
    var editInput = document.getElementById('editInput');
    var editButtons = document.getElementById('editButtons');

    // Set up the input field for editing
    editInput.innerHTML = `<input type="text" id="editField" value="${currentValue}" data-original-element="${elementId}" />`;

    // Show the input field and buttons
    editInput.style.display = 'block';
    editButtons.style.display = 'flex';

    // Hide the original text
    document.getElementById(elementId).style.display = 'none';
    console.log(`Editing triggered for element with ID: ${elementId}`);
}


function showEditInput(elementId) {
    // Check if the clicked element is not the pencil icon
    if (event.target.tagName !== 'I' || !event.target.classList.contains('bi-pencil-square')) {
        enableEditing(elementId);
    }
}

function cancelEditing() {
    var editInput = document.getElementById('editInput');
    var editButtons = document.getElementById('editButtons');
    var originalElement = document.getElementById('editField').getAttribute('data-original-element');
    
    // Clear the input field
    editInput.innerHTML = '';

    // Hide the input field and buttons
    editInput.style.display = 'none';
    editButtons.style.display = 'none';

    // Show the original text
    document.getElementById(originalElement).style.display = 'inline'; // Change to 'inline' to maintain inline layout
}

function saveChanges() {
    var editInput = document.getElementById('editInput');
    var editButtons = document.getElementById('editButtons');
    var elementId = document.getElementById('editField').getAttribute('data-original-element');

    // Get the edited value
    var editedValue = document.getElementById('editField').value;

    // Update the original text with the edited value
    document.getElementById(elementId).innerText = editedValue;

    // Clear the input field
    editInput.innerHTML = '';

    // Hide the input field and buttons
    editInput.style.display = 'none';
    editButtons.style.display = 'none';

    // Show the original text
    document.getElementById(elementId).style.display = 'inline'; // Change to 'inline' to maintain inline layout
}

function savePasswordChanges() {
    // Get the new password from the form
    var newPassword = document.getElementById("newPassword").value;
  
    // Add logic to save the new password (e.g., using AJAX to send it to the server)
  
    // Close the modal
    $('#changePasswordModal').modal('hide');
  }

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

function validateOldPw(){
    const pwform = document.forms['changpw'];
    const oldpwElement = pwform['oldPassword'];
    const oldpw = oldpwElement.value;
    var oldPasswordError = document.getElementById("oldPasswordError");
    axios.post('/validate/oldpw', {oldpw:oldpw}
    )
    .then((response) => {
      if(response.data.validatepw == "false") {
        oldPasswordError.innerText = "Passwords do not match. Please re-enter.";
        document.getElementById("myBtn").disabled = true;
      } else {
        oldPasswordError.innerText = '';
        document.getElementById("myBtn").disabled = false;
      }
    }, (error) => {
      console.log(error)
    })
  }

  function validateNewPw() {
    var newPassword = document.getElementById("newPassword").value;
    var newPasswordError = document.getElementById("newPasswordError");

    if (newPassword.length < 8) {
        newPasswordError.innerText = "Password must be at least 8 characters.";
        document.getElementById("myBtn").disabled = true;
    } else {
        newPasswordError.innerText = "";
        document.getElementById("myBtn").disabled = false;
    }

  }

  function validateNewMatch() {
    var newPassword = document.getElementById("newPassword").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    if (confirmPassword !== newPassword) {
        confirmPasswordError.innerText = "Passwords do not match. Please re-enter.";
        document.getElementById("myBtn").disabled = true;
    } else {
      confirmPasswordError.innerText = "";
      document.getElementById("myBtn").disabled = false;
    }
  }

  function validateOldNewMatch() {
    var newPassword = document.getElementById("newPassword").value;
    var oldPassword = document.getElementById("oldPassword").value;
    var newPasswordError = document.getElementById("newPasswordError");
    if (oldPassword == newPassword) {
      newPasswordError.innerText = "New password is the same as current password. Please try again";
      document.getElementById("myBtn").disabled = true;
    } else {
      newPasswordError.innerText = "";
      document.getElementById("myBtn").disabled = false;
    }
  }
