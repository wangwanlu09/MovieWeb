     //Recieve the values that users enter in front end
     function validateUsernamePassword() {
        var username = document.getElementById("username").value;
        var confirm_username = document.getElementById("confirm_username").value;
        var firstname = document.getElementById("firstname").value;
        var lastname = document.getElementById("lastname").value;
        var phone = document.getElementById("phone").value;
        var password1 = document.getElementById("password1").value;
        var password2 = document.getElementById("password2").value

        var namePattern = /^[A-Za-z]+$/;
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        var phonePattern = /^[0-9]{9,11}$/; 
        var passwordPattern = /(?=.*\d)(?=.*[a-z]).{8,}$/; 

        // Validate username existence and username pattern
        if (usernames.some(user => user.username.toLowerCase() === username.toLowerCase())) {
          document.getElementById("username-error").innerText = "Username already exists!";
          return false;
        } else if (!emailPattern.test(username)) {
          document.getElementById("username-error").innerText = "Invalid email address!";
          return false;
        } else {
          document.getElementById("username-error").innerText = "";  
        }
 
        // Validate username and confirm_username match
        if (username !== confirm_username) {
          document.getElementById("confirm_username-error").innerText = "Usernames do not match!";
          return false;
        } else {
          document.getElementById("confirm_username-error").innerText = "";
        }
  
        // Validate firstname value
        if (!namePattern.test(firstname)) {
          document.getElementById("firstname-error").innerText = "Please enter letters only!";
          return false;
        } else if (firstname.length > 25) {
          document.getElementById("firstname-error").innerText = "First Name should not exceed 25 characters!";
        } else {
          document.getElementById("firstname-error").innerText = "";  
        }

         // Validate lastname value
        if (!namePattern.test(lastname)) {
          document.getElementById("lastname-error").innerText = "Please enter letters only!";
          return false;
        } else if (lastname.length > 25) {
          document.getElementById("lastname-error").innerText = "Surname should not exceed 25 characters!";
        } else {
          document.getElementById("lastname-error").innerText = "";  
        }
        // validate phone pattern
        if (!phonePattern.test(phone)) {
          document.getElementById("phone-error").innerText = "Invalid phone number! Please enter 9 to 11 digits.";
          return false;
        } else {
          document.getElementById("phone-error").innerText = "";
        }

        // Validate password pattern
        if(!passwordPattern.test(password1)) {
          document.getElementById("password-error").innerText = "Must contain at least one number and one uppercase and lowercase letter,and at least 8 characters!";
          return false;
        } else {
          document.getElementById("password-error").innerText = "";
        }

        // Validate password match
        if (password1 !== password2) {
          document.getElementById("password-error").innerText = "Passwords do not match!";
          return false;
        } else {
          document.getElementById("password-error").innerText = "";
        }
  
        return { username,confirm_username,firstname,lastname,phone,password1, password2};
      }
     
      // A function to check if a password is strong enough
      function checkPassword(password1) {
        // Check the length, uppercase letter, and number
        if (password1.length < 8 || password1.length > 20 || !/[A-Z]/.test(password1) || !/[0-9]/.test(password1) || hasConsecutiveCharacters(password1)) {
            document.getElementById("password-error").innerText = "Password must be 8 to 20 characters long, contain at least one uppercase letter and one number, and avoid consecutive characters!";
            return false;
        }
    
        // Password passed all checks
        return true;
    }
    
    // Function to check for consecutive characters
    function hasConsecutiveCharacters(password1) {
      for (let i = 0; i < password1.length - 2; i++) {
          if (password1.charCodeAt(i) === password1.charCodeAt(i + 1) - 1 && password1.charCodeAt(i) === password1.charCodeAt(i + 2) - 2) {
              document.getElementById("password-error").innerText = "Avoid consecutive characters!";
              return true;
          }
      }
  
      // No consecutive characters found 
      return false;
  }


  function sendDateToBackendAndNavigate() {
      // Perform validation before submitting the form
      var isValid = validateUsernamePassword();
      var password1 = document.getElementById("password1").value; // Retrieve password1 value
      var checkPwd = checkPassword(password1); // Pass password1 to checkPassword
      var conse_pwd= hasConsecutiveCharacters(password1);

      if (isValid && checkPwd && !conse_pwd) {
          // If validation passes, submit the form
          document.getElementById("myFormId").submit();
      } 
    }