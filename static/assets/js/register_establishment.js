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
    for (var i = 0; i < vendorCount; i++) {
        var vendorDiv = document.createElement('div');
        vendorDiv.className = 'details vendor';

        // Add the required fields for each vendor (customize as needed)
        vendorDiv.innerHTML = `
            <span>Vendor ${i + 1} Details</span>
            <div class="fields">
                <div class="input-field">
                    <label>Name</label>
                    <input type="text" name="form-${i}-vendor_name" placeholder="Enter Vendor Name" >
                </div>

                <div class="input-field">
                    <label>Base Location (Head Office)</label>
                    <input type="text" name="form-${i}-vendor_base_location" placeholder="Enter Base Location" >
                </div>


                <div class="input-field">
                    <label>No. of Employees</label>
                    <input type="number" name="form-${i}-vendor_employees" placeholder="Enter No. of Employees" >
                </div>
                
                <div class="input-field">
                    <label>Male Employees</label>
                    <input type="number" name="form-${i}-vendor_male_employees" placeholder="Enter No. of Male Employees" >
                </div>

                <div class="input-field">
                    <label>Female Employees</label>
                    <input type="number" name="form-${i}-vendor_female_employees" placeholder="Enter No. of Female Employees" >
                </div>

                <div class="input-field">
                    <label>Others</label>
                    <input type="number" name="form-${i}-vendor_others" placeholder="Enter No. of Others" >
                </div>
            </div>
            <div class="details address">
            <div class="input-field address-field">
                <label>Address</label>
                <textarea type="text" name="form-${i}-vendor_address" cols="40" rows="5" placeholder="Enter Address" ></textarea>
            </div>
        </div>
        `;

        vendorDetailsSection.appendChild(vendorDiv);
    }
    // Append the form management fields
    var totalForms = document.createElement('input');
    totalForms.type = 'hidden';
    totalForms.name = 'form-TOTAL_FORMS';
    totalForms.value = vendorCount;

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

    vendorDetailsSection.appendChild(totalForms);
    vendorDetailsSection.appendChild(initialForms);
    vendorDetailsSection.appendChild(minNumForms);
    vendorDetailsSection.appendChild(maxNumForms);
}

function generateSiteDetails(){
    var siteCount = document.getElementById('siteCount').value;
    var siteDetailsSection = document.getElementById('siteDetailsSection');

    // Clear previous content
    siteDetailsSection.innerHTML = '';

    // Generate vendor details based on the count
    for (var i = 0; i < siteCount; i++) {
        var siteDiv = document.createElement('div');
        siteDiv.className = 'details site';

        // Add the required fields for each vendor (customize as needed)
        siteDiv.innerHTML = `
            <span>Site/Principal Employer ${i + 1} Details</span>
            <div class="fields">
                <div class="input-field">
                    <label>Name</label>
                    <input type="text" name="form-${i}-site_name" placeholder="Enter  Name">
                </div>

                <div class="input-field">
                    <label>Location</label>
                    <input type="text" name="form-${i}-site_location" placeholder="Enter Location">
                </div>

                <div class="input-field">
                    <label>No. of Employees Deployed</label>
                    <input type="number" name="form-${i}-deployed_employees" placeholder="Enter No. of Employees">
                </div>
                
                <div class="input-field">
                    <label>Male Employees</label>
                    <input type="number" name="form-${i}-deployed_male_employees" placeholder="Enter No. of Male Employees">
                </div>

                <div class="input-field">
                    <label>Female Employees</label>
                    <input type="number" name="form-${i}-deployed_female_employees" placeholder="Enter No. of Female Employees">
                </div>

                <div class="input-field">
                    <label>Others</label>
                    <input type="number" name="form-${i}-deployed_others" placeholder="Enter No. of Others">
                </div>
            </div>
            <div class="details address">
            <div class="input-field address-field">
                <label>Official Address</label>
                <textarea type="text" name="form-${i}-site_address" cols="40" rows="5" placeholder="Enter Address"></textarea>
            </div>
        </div>
        `;

        siteDetailsSection.appendChild(siteDiv);
    }
    // Append the form management fields
    var totalForms = document.createElement('input');
    totalForms.type = 'hidden';
    totalForms.name = 'form-TOTAL_FORMS';
    totalForms.value = siteCount;

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

    siteDetailsSection.appendChild(totalForms);
    siteDetailsSection.appendChild(initialForms);
    siteDetailsSection.appendChild(minNumForms);
    siteDetailsSection.appendChild(maxNumForms);
}

function generateLocationDetails() {
    var locationCount = document.getElementById('locationCount').value;
    var locationDetailsSection = document.getElementById('locationDetailsSection');

    // Clear previous content
    locationDetailsSection.innerHTML = '';

    // Generate vendor details based on the count
    for (var i = 0; i < locationCount; i++) {
        var locationDiv = document.createElement('div');
        locationDiv.className = 'details location';

        // Add the required fields for each vendor (customize as needed)
        locationDiv.innerHTML = `
            <span>Location ${i + 1} Details</span>
            <div class="fields">
                <div class="input-field">
                    <label>State</label>
                    <select name='form-${i}-locstate' onchange="print_city('state_${i}', this.selectedIndex);" id="sts_${i}" class="form-control"></select>
                </div>

                <div class="input-field">
                    <label>City</label>
                    <select name='form-${i}-loccity' id ="state_${i}" class="form-control" ></select>
                </div>

                <div class="input-field">
                    <label>Pincode</label>
                    <input type="number" name='form-${i}-locpincode' placeholder="Enter Pincode" class="form-control">
                </div>
            </div>

        `;


        locationDetailsSection.appendChild(locationDiv);

        // Call the functions after creating the elements
        print_state(`sts_${i}`);
    }
        // Append the form management fields
        var totalForms = document.createElement('input');
        totalForms.type = 'hidden';
        totalForms.name = 'form-TOTAL_FORMS';
        totalForms.value = locationCount;
    
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

        locationDetailsSection.appendChild(totalForms);
        locationDetailsSection.appendChild(initialForms);
        locationDetailsSection.appendChild(minNumForms);
        locationDetailsSection.appendChild(maxNumForms);
}
