$(document).ready(function () {
    const defaultProfileImage = "/static/assets/img/default_profile.svg";
    // File input change event
    $('#uploadPhoto').on('change', function (e) {
        const input = e.target;
        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                // Update the src attribute of the image
                $('#profile-image').attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    // Reset button click event
    $('#resetPhoto').on('click', function () {
        // Reset the image to the default profile pic
        $('#profile-image').attr('src', defaultProfileImage);
        // Clear the file input value to allow re-uploading the same file
        $('#uploadPhoto').val('');
    });
});


function addCommitteeField() {
    var comitteeCount = document.getElementById('comitteeCount').value;
    var comitteeDetailsSection = document.getElementById('committeesDetailsSection');

    // Count existing committee fields
    var currentCount = comitteeDetailsSection.getElementsByClassName('details comittee').length;

    // If the current count is less than the total count, add a new field
    if (currentCount < comitteeCount) {
        var comitteeDiv = document.createElement('div');
        comitteeDiv.className = 'details comittee';
        comitteeDiv.id = `committee-${currentCount}`;

        // Add the required fields for each committee
        comitteeDiv.innerHTML = `
        <div class="fields" style="margin-top: 20px">
            <label>Committee UID</label>
            <div class="input-field d-flex align-items-center">
                <input name='form-${currentCount}-comittee_uid' id="committee-${currentCount}-comittee_uid" class="form-control mr-2" placeholder="Enter UID if Committee is registered on MyPosh"></input>
                <button type="button" class="btn btn-danger" onclick="removeCommitteeField(${currentCount})">Remove</button>
            </div>
        </div>
    `;

        comitteeDetailsSection.appendChild(comitteeDiv);

        // Update form management fields
        updateFormManagementFields(comitteeCount);
    }
}

function updateFormManagementFields(totalCount) {
    var comitteeDetailsSection = document.getElementById('committeesDetailsSection');

    // Clear previous form management fields
    var oldManagementFields = comitteeDetailsSection.querySelectorAll('input[type="hidden"]');
    oldManagementFields.forEach(function(field) {
        field.remove();
    });

    // Append the form management fields
    var totalForms = document.createElement('input');
    totalForms.type = 'hidden';
    totalForms.name = 'form-TOTAL_FORMS';
    totalForms.value = totalCount;

    var initialForms = document.createElement('input');
    initialForms.type = 'hidden';
    initialForms.name = 'form-INITIAL_FORMS';
    initialForms.value = 0;

    var minNumForms = document.createElement('input');
    minNumForms.type = 'hidden';
    minNumForms.name = 'form-MIN_NUM_FORMS';
    minNumForms.value = 0;

    var maxNumForms = document.createElement('input');
    maxNumForms.type = 'hidden';
    maxNumForms.name = 'form-MAX_NUM_FORMS';
    maxNumForms.value = 1000;

    comitteeDetailsSection.appendChild(totalForms);
    comitteeDetailsSection.appendChild(initialForms);
    comitteeDetailsSection.appendChild(minNumForms);
    comitteeDetailsSection.appendChild(maxNumForms);
}

function removeCommitteeField(index) {
    var committeeDiv = document.getElementById(`committee-${index}`);
    if (committeeDiv) {
        committeeDiv.remove();
        
        // Update form management fields to reflect the change
        var comitteeCount = document.getElementById('comitteeCount').value;
        updateFormManagementFields(comitteeCount);
    }
}


// Top 5 clients
function addClientsField() {
    var clientDetailsSection = document.getElementById('clientDetailsSection');

    // Count existing client fields
    var currentCount = clientDetailsSection.getElementsByClassName('details client').length;

    // If the current count is less than 4 and less than the entered client count, add a new field
    if (currentCount < 5) {
        var clientDiv = document.createElement('div');
        clientDiv.className = 'details client';
        clientDiv.id = `client-${currentCount}`;

        // Add the required fields for each client
        clientDiv.innerHTML = `
            <div class="fields" style="margin-top: 20px">
                <label>Client Name</label>
                <div class="input-field d-flex align-items-center">
                    <input name='form-${currentCount}-client_name' id="client-${currentCount}-client_name" class="form-control mr-2" placeholder="Enter name of the client"></input>
                    <button type="button" class="btn btn-danger" onclick="removeClientField(${currentCount})">Remove</button>
                </div>
            </div>
        `;

        clientDetailsSection.appendChild(clientDiv);

        // Update form management fields
        updateFormManagementFields(currentCount + 1);
    }
}

function updateFormManagementFields(totalCount) {
    var clientDetailsSection = document.getElementById('clientDetailsSection');

    // Clear previous form management fields
    var oldManagementFields = clientDetailsSection.querySelectorAll('input[type="hidden"]');
    oldManagementFields.forEach(function(field) {
        field.remove();
    });

    // Append the form management fields
    var totalForms = document.createElement('input');
    totalForms.type = 'hidden';
    totalForms.name = 'form-TOTAL_FORMS';
    totalForms.value = totalCount;

    var initialForms = document.createElement('input');
    initialForms.type = 'hidden';
    initialForms.name = 'form-INITIAL_FORMS';
    initialForms.value = 0;

    var minNumForms = document.createElement('input');
    minNumForms.type = 'hidden';
    minNumForms.name = 'form-MIN_NUM_FORMS';
    minNumForms.value = 0;

    var maxNumForms = document.createElement('input');
    maxNumForms.type = 'hidden';
    maxNumForms.name = 'form-MAX_NUM_FORMS';
    maxNumForms.value = 1000;

    clientDetailsSection.appendChild(totalForms);
    clientDetailsSection.appendChild(initialForms);
    clientDetailsSection.appendChild(minNumForms);
    clientDetailsSection.appendChild(maxNumForms);
}

function removeClientField(index) {
    var clientDiv = document.getElementById(`client-${index}`);
    if (clientDiv) {
        clientDiv.remove();
        
        // Update form management fields to reflect the change
        var currentCount = document.getElementById('clientDetailsSection').getElementsByClassName('details client').length;
        updateFormManagementFields(currentCount);
    }
}


// document.getElementById('association').addEventListener('change', function () {
//     var associationSection = document.getElementById('associationSection');
//     var firmnameInput = document.getElementById('firmname');
//     var firmuidInput = document.getElementById('firmuid');

//     if (this.value === 'yes') {
//         associationSection.style.display = 'block';
//     } else {
//         associationSection.style.display = 'none';
//         firmnameInput.value = '';
//         firmuidInput.value = '';
//     }
// });

document.addEventListener('DOMContentLoaded', function() {
    var associationElement = document.getElementById('association');
    if (associationElement) {
        associationElement.addEventListener('change', function() {
            var associationSection = document.getElementById('associationSection');
            var firmnameInput = document.getElementById('firmname');
            var firmuidInput = document.getElementById('firmuid');

            if (this.value === 'yes') {
                associationSection.style.display = 'block';
            } else {
                associationSection.style.display = 'none';
                firmnameInput.value = '';
                firmuidInput.value = '';
            }
        });
    } 
});



function addMemberField() {
    var comitteeCount = document.getElementById('memberCount').value;
    var comitteeDetailsSection = document.getElementById('membersDetailsSection');

    // Count existing committee fields
    var currentCount = comitteeDetailsSection.getElementsByClassName('details member').length;

    // If the current count is less than the total count, add a new field
    if (currentCount < comitteeCount) {
        var comitteeDiv = document.createElement('div');
        comitteeDiv.className = 'details member';
        comitteeDiv.id = `member-${currentCount}`;

        // Add the required fields for each committee
        comitteeDiv.innerHTML = `
        <div class="fields" style="margin-top: 20px">
            <label>Member UID</label>
            <div class="input-field d-flex align-items-center">
                <input name='form-${currentCount}-member_uid' id="committee-${currentCount}-member_uid" class="form-control mr-2" placeholder="Enter UID if Member is registered on MyPosh"></input>
                <button type="button" class="btn btn-danger" onclick="removeMemberField(${currentCount})">Remove</button>
            </div>
        </div>
    `;

        comitteeDetailsSection.appendChild(comitteeDiv);

        // Update form management fields
        updateFormManageFields(comitteeCount);
    }
}

function updateFormManageFields(totalCount) {
    var comitteeDetailsSection = document.getElementById('membersDetailsSection');

    // Clear previous form management fields
    var oldManagementFields = comitteeDetailsSection.querySelectorAll('input[type="hidden"]');
    oldManagementFields.forEach(function(field) {
        field.remove();
    });

    // Append the form management fields
    var totalForms = document.createElement('input');
    totalForms.type = 'hidden';
    totalForms.name = 'form-TOTAL_FORMS';
    totalForms.value = totalCount;

    var initialForms = document.createElement('input');
    initialForms.type = 'hidden';
    initialForms.name = 'form-INITIAL_FORMS';
    initialForms.value = 0;

    var minNumForms = document.createElement('input');
    minNumForms.type = 'hidden';
    minNumForms.name = 'form-MIN_NUM_FORMS';
    minNumForms.value = 0;

    var maxNumForms = document.createElement('input');
    maxNumForms.type = 'hidden';
    maxNumForms.name = 'form-MAX_NUM_FORMS';
    maxNumForms.value = 1000;

    comitteeDetailsSection.appendChild(totalForms);
    comitteeDetailsSection.appendChild(initialForms);
    comitteeDetailsSection.appendChild(minNumForms);
    comitteeDetailsSection.appendChild(maxNumForms);
}

function removeMemberField(index) {
    var committeeDiv = document.getElementById(`member-${index}`);
    if (committeeDiv) {
        committeeDiv.remove();
        
        // Update form management fields to reflect the change
        var comitteeCount = document.getElementById('memberCount').value;
        updateFormManageFields(comitteeCount);
    }
}

