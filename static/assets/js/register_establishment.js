document.getElementById('natureOfEstablishment').addEventListener('change', function () {
    var principalEmployerSection = document.getElementById('principalEmployerSection');
    var vendorSection = document.getElementById('vendorSection');
    var prin = document.getElementById('prin-title');
    var ven = document.getElementById('ven-title');

    // Reset visibility
    // principalEmployerSection.style.display = 'none';
    // vendorSection.style.display = 'none';

    // Show relevant section based on the selected option
    var selectedOption = this.value;
    if (selectedOption === 'principal') {
        principalEmployerSection.style.display = 'block';
        vendorSection.style.display = 'none';
        prin.style.display = 'none'
        ven.style.display = 'none'
    } else if (selectedOption === 'vendor') {
        principalEmployerSection.style.display = 'none';
        vendorSection.style.display = 'block';
        prin.style.display = 'none'
        ven.style.display = 'none'
    }
    else if (selectedOption === 'both'){
        principalEmployerSection.style.display = 'block';
        vendorSection.style.display = 'block';
        prin.style.display = 'block'
        ven.style.display = 'block'
    }
});

function generateVendorDetails() {
    var vendorCount = document.getElementById('vendorCount').value;
    var vendorDetailsSection = document.getElementById('vendorDetailsSection');

    // Clear previous content
    vendorDetailsSection.innerHTML = '';

    // Generate vendor details based on the count
    for (var i = 1; i <= vendorCount; i++) {
        var vendorDiv = document.createElement('div');
        vendorDiv.className = 'details location';

        // Add the required fields for each vendor (customize as needed)
        vendorDiv.innerHTML = `
            <span>Vendor ${i} Details</span>
            <div class="fields">
                <div class="input-field">
                    <label>Name</label>
                    <input type="text" name="vendor_name_${i}" placeholder="Enter Vendor Name" required>
                </div>

                <div class="input-field">
                    <label>Base Location (Head Office)</label>
                    <input type="text" name="vendor_base_location_${i}" placeholder="Enter Base Location" required>
                </div>


                <div class="input-field">
                    <label>No. of Employees</label>
                    <input type="number" name="vendor_employees_${i}" placeholder="Enter No. of Employees" required>
                </div>
                
                <div class="input-field">
                    <label>Male Employees</label>
                    <input type="number" name="vendor_male_employees_${i}" placeholder="Enter No. of Male Employees" required>
                </div>

                <div class="input-field">
                    <label>Female Employees</label>
                    <input type="number" name="vendor_female_employees_${i}" placeholder="Enter No. of Female Employees" required>
                </div>

                <div class="input-field">
                    <label>Others</label>
                    <input type="number" name="vendor_others_${i}" placeholder="Enter No. of Others" required>
                </div>
            </div>
            <div class="details address">
            <div class="input-field address-field">
                <label>Address</label>
                <textarea type="text" name="address" cols="40" rows="5" placeholder="Enter Address" required></textarea>
            </div>
        </div>
        `;

        vendorDetailsSection.appendChild(vendorDiv);
    }
}

function generateSiteDetails(){
    var siteCount = document.getElementById('siteCount').value;
    var siteDetailsSection = document.getElementById('siteDetailsSection');

    // Clear previous content
    siteDetailsSection.innerHTML = '';

    // Generate vendor details based on the count
    for (var i = 1; i <= siteCount; i++) {
        var siteDiv = document.createElement('div');
        siteDiv.className = 'details location';

        // Add the required fields for each vendor (customize as needed)
        siteDiv.innerHTML = `
            <span>Site/Principal Employer ${i} Details</span>
            <div class="fields">
                <div class="input-field">
                    <label>Name</label>
                    <input type="text" name="site_name_${i}" placeholder="Enter  Name" required>
                </div>

                <div class="input-field">
                    <label>Location</label>
                    <input type="text" name="site_location_${i}" placeholder="Enter Location" required>
                </div>

                <div class="input-field">
                    <label>No. of Employees Deployed</label>
                    <input type="number" name="deployed_employees_${i}" placeholder="Enter No. of Employees" required>
                </div>
                
                <div class="input-field">
                    <label>Male Employees</label>
                    <input type="number" name="deployed_male_employees_${i}" placeholder="Enter No. of Male Employees" required>
                </div>

                <div class="input-field">
                    <label>Female Employees</label>
                    <input type="number" name="deployed_female_employees_${i}" placeholder="Enter No. of Female Employees" required>
                </div>

                <div class="input-field">
                    <label>Others</label>
                    <input type="number" name="deployed_others_${i}" placeholder="Enter No. of Others" required>
                </div>
            </div>
            <div class="details address">
            <div class="input-field address-field">
                <label>Official Address</label>
                <textarea type="text" name="address" cols="40" rows="5" placeholder="Enter Address" required></textarea>
            </div>
        </div>
        `;

        siteDetailsSection.appendChild(siteDiv);
    }
}

function generateLocationDetails() {
    var locationCount = document.getElementById('locationCount').value;
    var locationDetailsSection = document.getElementById('locationDetailsSection');

    // Clear previous content
    locationDetailsSection.innerHTML = '';

    // Generate vendor details based on the count
    for (var i = 1; i <= locationCount; i++) {
        var locationDiv = document.createElement('div');
        locationDiv.className = 'details location';

        // Add the required fields for each vendor (customize as needed)
        locationDiv.innerHTML = `
            <span>Location ${i} Details</span>
            <div class="fields">
                <div class="input-field">
                    <label>State</label>
                    <select name='state' onchange="print_city('state_${i}', this.selectedIndex);" id="sts_${i}" name="stt_${i}" class="form-control" required></select>
                </div>

                <div class="input-field">
                    <label>City</label>
                    <select name='city_${i}' id ="state_${i}" class="form-control" required ></select>
                </div>

                <div class="input-field">
                    <label>Pincode</label>
                    <input type="number" name='pincode' placeholder="Enter Pincode" required>
                </div>
            </div>
        `;

        locationDetailsSection.appendChild(locationDiv);

        // Call the functions after creating the elements
        print_state(`sts_${i}`);
    }
}
