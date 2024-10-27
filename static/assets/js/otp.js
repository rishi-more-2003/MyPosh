const inputs = document.querySelectorAll(".otp-card-inputs input");
const button = document.querySelector('.otp-card button');


inputs.forEach(input => {
  let lastInputStatus = 0;

  input.onkeyup = (e) => {
    const currentElement = e.target;
    const nextElement = input.nextElementSibling;
    const prevElement = input.previousElementSibling;

    if (prevElement && e.keyCode === 8) {
      if (lastInputStatus === 1) {
        prevElement.value = "";
        prevElement.focus();
      }
      button.setAttribute("disabled", true);
      lastInputStatus = 1;
    } else {
      const reg = /^[0-9]+$/;
      if (!reg.test(currentElement.value)) {
        currentElement.value = currentElement.value.replace(/\D/g, '');
      } else if (currentElement.value) {
        if (nextElement) {
          nextElement.focus();
        } else {
          button.removeAttribute('disabled');
          lastInputStatus = 0;
        }
      }
    }
  };
});

var timeLeft = 30;
var timerElement = document.getElementById('timer');
var resendLink = document.getElementById('resend-link');
var otpMessage = document.getElementById('otp-message');
var resendMessage = document.getElementById('resend-message');
var timerId;  // Moved outside to access globally

function startTimer() {
    // Reset timer values
    timeLeft = 30;
    resendLink.style.pointerEvents = 'none'
    // Clear any existing interval
    clearInterval(timerId);

    // Start new timer
    timerId = setInterval(countdown, 1000);
}

function resendstartTimer() {
  // Reset timer values
  timeLeft = 30;

  resendMessage.innerHTML = "If you haven't received the OTP yet, you can request it again.<span id='timer'></span></p> "

  // Get reference to the timer <span> after setting the innerHTML
  timerElement = document.getElementById('timer');
  
  resendLink.style.pointerEvents = 'none'
  // Clear any existing interval
  clearInterval(timerId);

  // Start new timer
  timerId = setInterval(countdown, 1000);
}

function countdown() {
    if (timeLeft == -1) {
        clearTimeout(timerId);
        resendLink.style.pointerEvents = 'auto'
        resendLink.style.cursor = 'pointer'
        resendLink.style.color = 'green'; 
        resendMessage.innerHTML = 'Click below to resend';
    } else {
        timerElement.innerHTML = ' (' + timeLeft + 's)';
        timeLeft--;
        resendLink.style.color = 'gray'; 
    }
}

const overlay = document.getElementById('overlay');
let popup = document.getElementById('otp-popup');

function openPopup(){
    popup.classList.add("open-popup");  
    overlay.style.display = 'block';
    startTimer();  // Reset and start the timer whenever popup opens
}

function closePopup(){
    popup.classList.remove("open-popup"); 
    overlay.style.display = 'none';
}


