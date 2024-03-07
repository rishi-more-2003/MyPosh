const toggle = document.querySelector(".toggle");
const passwordInput = document.querySelector(".input-field .flexble input[type='password']");

toggle.addEventListener("click", () => {
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggle.classList.replace("ri-eye-off-fill", "ri-eye-fill");
    } else {
        passwordInput.type = "password";
        toggle.classList.replace("ri-eye-fill", "ri-eye-off-fill");
    }
});

const submitButton = document.getElementById('submitButton');
const requiredFields = document.querySelectorAll('input[required]');

// Check if all required fields are filled initially
submitButton.disabled = !areAllFieldsFilled();

function areAllFieldsFilled() {
  for (const field of requiredFields) {
    if (field.value.trim() === '') {
      return false; // If any field is empty, return false
    }
  }
  return true; // If all fields are filled, return true
}

// Event listener to update button state on input change
for (const field of requiredFields) {
  field.addEventListener('input', function() {
    submitButton.disabled = !areAllFieldsFilled();
  });
}

