// // Date-picker
// var today = new Date().toISOString().split('T')[0];
// document.getElementById('date-input').setAttribute('max', today)

// // Email-Validator
// const emailId = document.getElementById("email-id");
// const  errorsMsg = document.getElementById("error-msg");
//     // Disable-button-until-form
//     validateButtonOne = document.querySelector(".ValBtn.one");
//     mailRegex = /^[a-zA-Z][a-zA-Z0-9\-\_\.]+@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}$/;
//     validateButtonOne.style.backgroundColor = 'hsl(29, 54%, 73%)';

// function checker(){
//     if(emailId.value.match(mailRegex)){
//         errorsMsg.style.display = 'none';
//         emailId.style.border = '2px solid #2ecc71';
//         validateButtonOne.removeAttribute('disabled');
//         validateButtonOne.style.backgroundColor = 'hsl(30, 100%, 52%)';
//         return emailId.value.match(mailRegex);
//     }
//     else if(emailId.value == ""){
//         errorsMsg.style.display = 'none';
//         validateButtonOne.setAttribute('disabled', 'disabled');
//         validateButtonOne.style.backgroundColor = 'hsl(29, 54%, 73%)';
//         emailId.style.border = '2px solid #d1d3d4';
//     }
//     else{
//         validateButtonOne.style.backgroundColor = 'hsl(29, 54%, 73%)';
//         validateButtonOne.setAttribute('disabled', 'disabled');
//         errorsMsg.style.display = 'block';
//         emailId.style.border = '2px solid #ff2851';
//     }

// }

// // phone-country-code
// const phoneInputField = document.querySelector("#phone");
// const phoneInput = window.intlTelInput(phoneInputField,  {
//   utilsScript:
//     "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
//     preferredCountries: ['in'],
// });

// // Phone-validity
// const errorMsg = document.getElementById("errormsg");
//     // Disable-button-until-form
// const validateButtonTwo = document.querySelector(".ValBtn.two");
// validateButtonTwo.style.backgroundColor = 'hsl(29, 54%, 73%)';

// function checkerphone() {
//     const phoneNumberRegex = /^\d+$/;

//     if (phoneInputField.validity.valid && phoneNumberRegex.exec(phoneInputField.value)) {
//         errorMsg.style.display = 'none';
//         phoneInputField.style.border = '2px solid #2ecc71';
//         validateButtonTwo.removeAttribute('disabled');
//         validateButtonTwo.style.backgroundColor = 'hsl(30, 100%, 52%)';
//         return phoneInputField.validity.valid && phoneNumberRegex.exec(phoneInputField.value);

//     }  else if(phoneInputField.value === ""){
//         validateButtonTwo.style.backgroundColor = 'hsl(29, 54%, 73%)';
//         validateButtonTwo.setAttribute('disabled', 'disabled');
//         errorMsg.style.display = 'none';
//         phoneInputField.style.border = '2px solid #d1d3d4';
//     }
//     else {
//         errorMsg.style.display = 'block';
//         phoneInputField.style.border = '2px solid #ff2851';
//         validateButtonTwo.style.backgroundColor = 'hsl(29, 54%, 73%)';
//         validateButtonTwo.setAttribute('disabled', 'disabled');
//     }
// }

// const submitButton = document.getElementById('submitButton');
// const requiredFields = document.querySelectorAll('input[required]');

// // Check if all required fields are filled initially
// submitButton.disabled = !areAllFieldsFilled();

// function areAllFieldsFilled() {
//   for (const field of requiredFields) {
//     if (field.value.trim() === '') {
//       return false; // If any field is empty, return false
//     }
//   }
//   return true; // If all fields are filled, return true
// }

// // Event listener to update button state on input change
// for (const field of requiredFields) {
//   field.addEventListener('input', function() {
//     submitButton.disabled = !areAllFieldsFilled() || !checker() || !checkerphone();;
//   });
// }

// const toggles = document.querySelectorAll(".toggle");
// const passwordInputs = document.querySelectorAll(".input-field .inp input[type='password']");

// toggles.forEach((toggle, index) => {
//     toggle.addEventListener("click", () => {
//         const passwordInput = passwordInputs[index];

//         if (passwordInput.type === "password") {
//             passwordInput.type = "text";
//             toggle.classList.replace("ri-eye-off-fill", "ri-eye-fill");
//         } else {
//             passwordInput.type = "password";
//             toggle.classList.replace("ri-eye-fill", "ri-eye-off-fill");
//         }
//     });
// });

// document.getElementById("sendOTP").addEventListener("click", function() {
//     var email = document.getElementById("email-id").value;
//     // Send AJAX request to Django view to send OTP
//     fetch("{% url 'register' %}", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": "{{ csrf_token }}"
//         },
//         body: JSON.stringify({ email: email })
//     })
//     .then(response => {
//         if (response.ok) {
//             // Display the OTP input field
//             document.querySelector(".otp-field").style.display = "block";
//         } else {
//             // Handle error response
//             console.error("Failed to send OTP");
//         }
//     })
//     .catch(error => {
//         console.error("Error:", error);
//     });
// });

