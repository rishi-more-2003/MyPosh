/* SHOW-MeNU */
const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')


// MENU-SHOW
// Validate if constant exists
if(navToggle){
    navToggle.addEventListener('click', () =>{
        navMenu.classList.add('show-menu')
    })
}

// MENU-CLOSE
// Validate if constant exists
if(navClose){
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}

// REMOVE MENU 
const navLink = document.querySelectorAll('.nav__link')

function linkAction(){
    const navMenu = document.getElementById('nav-menu')
    navMenu.classList.remove('show-menu')
}

navLink.forEach(n => n.addEventListener('click', linkAction))


// CHANGE-BACKGORUND-HEADER

function scrollHeader(){
    const header = document.getElementById('header')

    if(this.scrollY >= 80) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}

window.addEventListener('scroll', scrollHeader)

// FAQs
const accordionItems = document.querySelectorAll('.questions__item')

accordionItems.forEach((item) => {
    const accordionHeader = item.querySelector('.questions__header')

    accordionHeader.addEventListener('click', () =>{
        const openItem = document.querySelector('.accordion-open')
        toggleItem(item)

        if(openItem && openItem != item){
            toggleItem(openItem)
        }
    })
})

const toggleItem = (item) => {
    const accordionContent = item.querySelector('.questions__content')

    if(item.classList.contains('accordion-open')){
        accordionContent.removeAttribute('style')
        item.classList.remove('accordion-open')
    }else{
        accordionContent.style.height = accordionContent.scrollHeight + 'px'
        item.classList.add('accordion-open')
    }

}

// SCROLL SECTIONS ACTIVE LINK
const sections = document.querySelectorAll('section[id]')

function scrollActive(){
    const scrollY = window.pageYOffset

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight,
                sectionTop = current.offsetTop - 58,
                sectionId = current.getAttribute('id')

        if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
            document.querySelector('.nav__menu a[href*=' + sectionId +']').classList.add('active-link')
        }else{
            document.querySelector('.nav__menu a[href*=' + sectionId +']').classList.remove('active-link')
       
        }
    })
}
window.addEventListener('scroll', scrollActive)

// SCROLL-UP

function scrollUp(){
    const scrollUp = document.getElementById('scroll-up');
    if(this.scrollY >= 200) scrollUp.classList.add('show-scroll');
    else scrollUp.classList.remove('show-scroll')
}

window.addEventListener('scroll', scrollUp)

// DARK LIGHT THEME
// const themeButton = document.getElementById('theme-button')
// const darkTheme = 'dark-theme'
// const iconTheme = 'ri-sun-line'

// const selectedTheme = localStorage.getItem('selected-theme')
// const selectedIcon = localStorage.getItem('selected-icon')

// const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
// const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'ri-moon-line' : 'ri-sun-line'

// if (selectedTheme){
//     document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
//     themeButton.classList[selectedIcon === 'ri-moon-line' ? 'add' : 'remove'](iconTheme)
// } 

// themeButton.addEventListener('click', () => {
//     document.body.classList.toggle(darkTheme)
//     themeButton.classList.toggle(iconTheme)

//     localStorage.setItem('selected-theme', getCurrentTheme())
//     localStorage.setItem('selected-icon', getCurrentIcon())
// })

// SCROLL-REVEAL-ANIMATION
const sr = ScrollReveal({
    origin: 'bottom',
    distance: '60px',
    duration: 2500,
    delay: 400,
    // reset: true
})

sr.reveal(`.home__data`)
sr.reveal(`.home__img`, {delay: 500})
sr.reveal(`.about__img, .contact__box`, {origin: 'left', delay: 500})
sr.reveal(`.about__data, .contact__form`, {origin: 'right', delay: 500})
sr.reveal(`.steps__card, .questions__group, .footer`, {interval: 100})

// LOADER
onload = () => {
    const load = document.getElementById('load')

    setTimeout(() => {
        load.style.display = 'none'
    }, 500)
}



$('#ajaxSubmitButton').on('click', function(event) {
    event.preventDefault(); // Prevent default button action

    // Gather form data
    var formData = $('#verifyForm').serialize(); // Serialize form data including CSRF token

    // Send AJAX POST request to update skill details
    $.ajax({
        url: $('#verifyForm').attr('action'), // Get the action URL from the form
        type: 'POST',
        data: formData,
        success: function(response) {
            // Handle success (e.g., close modal, show success message)
            $('#myModal').modal('hide');
            location.reload(); // Reload the page to see the changes
        },
        error: function(xhr, errmsg, err) {
            // Handle error (e.g., show error message)
            console.log(errmsg);
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    // Get Elements
    const openPopupC = document.getElementById('openPopup-committee');
    const closePopupC = document.getElementById('closePopup-committee');
    const popupC = document.getElementById('popup-committee');

    const infoIcons = document.querySelectorAll(".info-btn");

    infoIcons.forEach(icon => {
      icon.addEventListener("click", () => {
        const targetId = icon.getAttribute("data-target");
        const infoContent = document.getElementById(targetId);
  
        // Toggle the visibility of the info content
        if (infoContent) {
          if (infoContent.style.display === "block") {
            infoContent.style.display = "none";
          } else {
            infoContent.style.display = "block";
          }
        }
      });
    });
    
    // Open Popup
    openPopupC.addEventListener('click', async () => {
        popupC.classList.remove('hidden-committee');
        try {
            const response = await fetch("/api/get-location-count/");
            if (response.ok) {
              const data = await response.json();
              const count = data.count; // Assuming the backend sends { count: <number> }
              updateButtonStates(count);
            } else {
              console.error("Failed to fetch data");
            }
          } catch (error) {
            console.error("Error:", error);
          }
    });

    // Close Popup
    closePopupC.addEventListener('click', () => {
        popupC.classList.add('hidden-committee');
    });

    // Close on Clicking Outside
    window.addEventListener('click', (event) => {
        if (event.target === popupC) {
            popupC.classList.add('hidden-committee');
        }
    });

    document.querySelectorAll('.info-btn').forEach((infoBtn) => {
        infoBtn.addEventListener('mouseenter', () => {
        const infoText = infoBtn.getAttribute('data-info');
        infoBtn.setAttribute('title', infoText);
        });
    });

    // Function to disable and style buttons
  const updateButtonStates = (count) => {
    const buttons = document.querySelectorAll(".option-committee");

    buttons.forEach((button) => {
      const optionId = button.getAttribute("data-option-id");
      const link = button.closest(".option-committee-link");
      const backcolor = button.closest(".option-info")

      button.disabled = false; // Reset all buttons
      button.style.backgroundColor = ""; // Reset styles
      if (link) link.classList.remove("disabled");

      if (count === 1 && optionId !== "single") {
        button.disabled = true;
        button.style.backgroundColor = "var(--first-color-alt)";
        button.style.color = "var(--text-color-light)";
        button.style.cursor = "not-allowed";
        if (backcolor){
            backcolor.style.backgroundColor =  "var(--first-color-alt)";
            backcolor.style.cursor = "not-allowed";
        }  
        if (link) link.classList.add("disabled");

      } else if (count > 1 && optionId === "single") {
        button.disabled = true;
        button.style.backgroundColor = "var(--first-color-alt)";
        button.style.color = "var(--text-color-light)";
        button.style.cursor = "not-allowed";
        if (backcolor){
            backcolor.style.backgroundColor =  "var(--first-color-alt)";
            backcolor.style.cursor = "not-allowed";
        }  
        if (link) link.classList.add("disabled");

      }
    });
  };

});

const multibtn = document.getElementById("multi-core-button");
const coremodal = document.getElementById("hierarchyModal");
const popupcommittee = document.getElementById("popup-committee");
const closecoremodal = document.getElementById("closeCoreModal");
const generateTree = document.getElementById("generateTree");
const hierarchyContainer = document.getElementById("hierarchyTree");
const numberInput = document.getElementById("numberInput");

multibtn.onclick = () => { 
    coremodal.style.display = "block";
};


// Close Modal
closecoremodal.onclick = () => {
    coremodal.style.display = "none";
    hierarchyContainer.innerHTML = ""; // Clear the hierarchy if modal closes
};

// Generate Hierarchy on Button Click
generateTree.onclick = () => {
    const levels = parseInt(numberInput.value, 10);
    if (isNaN(levels) || levels < 1) {
        alert("Please enter a valid number greater than 0.");
        return;
    }

    // Clear previous tree
    hierarchyContainer.innerHTML = "";

    const leftColumn = document.createElement("div");
    leftColumn.className = "left-column";

// Generate roles for each level
for (let i = 1; i <= levels; i++) {
    // Core External
    const coreExternal = `${'Sub '.repeat(i - 1)}Core External Member`;

    // Create a container for role and input
    const roleContainer = document.createElement("div");
    roleContainer.className = "role-row"; // Optional class for styling

    // Create and set up the role text
    const externalRole = document.createElement("p");
    externalRole.textContent = coreExternal;

    // Create the "Alias:" label
    const aliasLabel = document.createElement("span");
    aliasLabel.textContent = "Alias: ";
    aliasLabel.className = "alias-label"; // Optional class for styling

    // Create and set up the input field
    const externalInput = document.createElement("input");
    externalInput.type = "text";
    externalInput.placeholder = `Default ${coreExternal}`;
    externalInput.className = "role-input"; // Optional class for styling

    // Append the role, label, and input to the container
    roleContainer.appendChild(externalRole);
    roleContainer.appendChild(aliasLabel);
    roleContainer.appendChild(externalInput);

    // Append the container to the left column
    leftColumn.appendChild(roleContainer);
}

// Generate roles for each level
for (let i = 1; i <= levels; i++) {
    // Core Internal
    const coreInternal = `${'Sub '.repeat(i - 1)}Core Internal Member`;

    // Create a container for role and input
    const roleContainer = document.createElement("div");
    roleContainer.className = "role-row"; // Optional class for styling

    // Create and set up the role text
    const internalRole = document.createElement("p");
    internalRole.textContent = coreInternal;

    // Create the "Alias:" label
    const aliasLabel = document.createElement("span");
    aliasLabel.textContent = "Alias: ";
    aliasLabel.className = "alias-label"; // Optional class for styling

    // Create and set up the input field
    const internalInput = document.createElement("input");
    internalInput.type = "text";
    internalInput.placeholder = `Default ${coreInternal}`;
    internalInput.className = "role-input"; // Optional class for styling

    // Append the role, label, and input to the container
    roleContainer.appendChild(internalRole);
    roleContainer.appendChild(aliasLabel);
    roleContainer.appendChild(internalInput);

    // Append the container to the left column
    leftColumn.appendChild(roleContainer);
}

// Append columns to the hierarchy container
hierarchyContainer.appendChild(leftColumn);
const corebtn = document.createElement("button")
corebtn.className = "btn btn-success"
corebtn.id= "get-all-alias"
corebtn.textContent = "Save"
corebtn.onclick = function() { sendHierarchyData(); };

hierarchyContainer.appendChild(corebtn)

}

// Function to gather data and send to backend
function sendHierarchyData() {
    const hierarchyRows = document.querySelectorAll('.role-row'); // All role rows
    const hierarchyData = []; // Array to hold the data to send

    // Loop through each row
    hierarchyRows.forEach(row => {
        const roleText = row.querySelector('p').textContent; // Left column text
        const inputField = row.querySelector('input'); // Input field

        // Get the input value or default to the roleText if empty
        const alias = inputField.value.trim() || roleText;

        // Push the data to the array
        hierarchyData.push({
            role: roleText,
            alias: alias
        });
    });

    console.log(JSON.stringify(hierarchyData))

    // Send data to the backend via AJAX
    fetch('/multi-committee-multi-core-group-formation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Include CSRF token for Django (if using)
        },
        body: JSON.stringify(hierarchyData)
    })
    .then(response => {
        if (response.ok) {
            console.log("Response sent to the server");
            window.location.href = "/multi-committee-multi-core-group-formation/";
        } else {
            throw new Error('Error sending hierarchy data.');
        }
    })
    .then(data => {
        console.log('Data successfully sent:', data);
        // alert('Hierarchy data sent successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        // alert('Failed to send hierarchy data.');
    });
}

// Helper function to get CSRF token for Django (if applicable)
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}