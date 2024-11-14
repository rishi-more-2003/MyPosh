var next_click=document.querySelectorAll(".next_button");
var main_form=document.querySelectorAll(".main");
var step_list = document.querySelectorAll(".progress-bar li");
var num = document.querySelector(".step-number");
let formnumber=0;

next_click.forEach(function(next_click_form){
    next_click_form.addEventListener('click',function(){
        if(!validateform()){
            return false
        }
       formnumber++;
       updateform();
       progress_forward();
       contentchange();
    });
}); 

var back_click=document.querySelectorAll(".back_button");
back_click.forEach(function(back_click_form){
    back_click_form.addEventListener('click',function(){
       formnumber--;
       updateform();
       progress_backward();
       contentchange();
    });
});

var username=document.querySelector("#user_name");
var shownname=document.querySelector(".shown_name");
 

var submit_click=document.querySelectorAll(".submit_button");
submit_click.forEach(function(submit_click_form){
    submit_click_form.addEventListener('click',function(){
       shownname.innerHTML= username.value;
       formnumber++;
       updateform(); 
    });
});

// var heart=document.querySelector(".fa-heart");
// heart.addEventListener('click',function(){
//    heart.classList.toggle('heart');
// });


// var share=document.querySelector(".fa-share-alt");
// share.addEventListener('click',function(){
//    share.classList.toggle('share');
// });

 


function updateform(){
    main_form.forEach(function(mainform_number){
        mainform_number.classList.remove('active');
    })
    main_form[formnumber].classList.add('active');
} 
 
function progress_forward(){
    // step_list.forEach(list => {
        
    //     list.classList.remove('active');
         
    // }); 
    
     
    num.innerHTML = formnumber+1;
    step_list[formnumber].classList.add('active');
}  

function progress_backward(){
    var form_num = formnumber+1;
    step_list[form_num].classList.remove('active');
    num.innerHTML = form_num;
} 
 
var step_num_content=document.querySelectorAll(".step-number-content");

 function contentchange(){
     step_num_content.forEach(function(content){
        content.classList.remove('active'); 
        content.classList.add('d-none');
     }); 
     step_num_content[formnumber].classList.add('active');
 } 
 
 
function validateform(){
    validate=true;
    var validate_inputs=document.querySelectorAll(".main.active input");
    validate_inputs.forEach(function(vaildate_input){
        vaildate_input.classList.remove('warning');
        if(vaildate_input.hasAttribute('require')){
            if(vaildate_input.value.length==0){
                validate=false;
                vaildate_input.classList.add('warning');
            }
        }
    });
    return validate;
    
}

const optionBtn = document.getElementById("optionBtn");
const optionModal = document.getElementById("optionModal");
const closeBtn = document.getElementsByClassName("close")[0];

function closeModal() {
    optionModal.style.display = "none";
    // clearPreview();
}

function closeManual(){
    manualModal.style.display = "none";
}


function checkInput() {
    const countLoc = document.getElementById('countloc').value;
    if (countLoc > 0) {
        optionBtn.onclick = () => { optionModal.style.display = "block"};
        closeBtn.onclick = () => { closeModal(); };
        window.onclick = (e) => { if (e.target === optionModal) closeModal(); };
    } else {
        alert("Please enter a number greater than 0");
    }
}


const manualBtn = document.getElementById("manualBtn");
const manualModal = document.getElementById("manualModal");
const closeBtnn = document.getElementsByClassName("close-loc")[0];

manualBtn.onclick = () => {
    manualModal.style.display = "block";
    optionModal.style.display = "none";

    // Get the count from countloc
    const countloc = parseInt(document.getElementById('countloc').value, 10);
    const tbody = document.querySelector("#bootstrapdatatable tbody");

    // Clear any existing rows in the tbody
    tbody.innerHTML = '';

    // Add the specified number of empty rows
    for (let i = 0; i < countloc; i++) {
        const row = document.createElement("tr");
        
        row.innerHTML = `
            <td>${i + 1}</td>
            <td data-type="text" class="editable-cell"></td>
            <td data-type="text" class="editable-cell"></td>
            <td data-type="checkbox1" class="editable-cell"></td>
            <td data-type="number" class="editable-cell"></td>
            <td data-type="checkbox2" class="editable-cell"></td>
            <td data-type="number" class="editable-cell"></td>
            <td data-type="number" class="editable-cell"></td>
            <td class="but">
                <button class="btn btn-primary btn-sm save-btn d-none" onclick="saveRow(this)">Save</button>
                <button class="btn btn-secondary btn-sm edit-btn" onclick="editRow(this)">Edit</button>
                <button class="btn btn-danger btn-sm remove-btn" onclick="removeRow(this)">Remove</button>
            </td>
        `;
    
        // Append the new row to the tbody
        tbody.appendChild(row);
    }
};

closeBtnn.onclick = () => { closeManual(); };

document.addEventListener("DOMContentLoaded", function() {
    // Function to get URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const step = parseInt(urlParams.get("step")) || 1;

    // Function to show the correct step based on the parameter
    function showStep(step) {
        document.querySelectorAll(".step-number-content").forEach(content => {
            content.classList.toggle("active", content.getAttribute("data-step") == step);
            content.classList.toggle("d-none", content.getAttribute("data-step") != step);
        });
        document.querySelectorAll(".main").forEach(content => {
            content.classList.toggle("active", content.getAttribute("data-step") == step);
            content.classList.toggle("d-none", content.getAttribute("data-step") != step);
        });
        document.querySelectorAll(".progress-item").forEach((item, index) => {
            item.classList.toggle("active", index < step);
        });
        document.querySelector(".step-number").textContent = step;
    }

    // Initialize the correct step based on URL
    showStep(step);
});

const excelBtn = document.getElementById("excelBtn");
const excelModal = document.getElementById("excelModal");
const closeBtnnn = document.getElementsByClassName("close-excel")[0];

const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const previewContainer = document.getElementById("previewContainer");
const filePreview = document.getElementById("filePreview");

const uploadVendorArea = document.getElementById("uploadVendorArea");
const VendorfileInput = document.getElementById("VendorfileInput");
const previewVendorContainer = document.getElementById("previewVendorContainer");
const fileVendorPreview = document.getElementById("fileVendorPreview");

const uploadEmployeeArea = document.getElementById("uploadEmployeeArea");
const EmployeefileInput = document.getElementById("EmployeefileInput");
const previewEmployeeContainer = document.getElementById("previewEmployeeContainer");
const fileEmployeePreview = document.getElementById("fileEmployeePreview");

window.onclick = (e) => { if (e.target === excelModal) closeExcel(); };

excelBtn.onclick = () => {
    excelModal.style.display = "block";
    optionModal.style.display = "none";
    previewContainer.style.display = "none"
}

function closeExcel(){
    excelModal.style.display = "none";
}

closeBtnnn.onclick = () => { closeExcel(); };

// Upload Form

function clearPreview() {
    filePreview.innerHTML = "";
    // previewContainer.style.display = "none";
}

function clearVendorPreview() {
    fileVendorPreview.innerHTML = "";
    // previewContainer.style.display = "none";
}

function clearEmployeePreview() {
    fileEmployeePreview.innerHTML = "";
    // previewContainer.style.display = "none";
}

// Drag and Drop functionality
uploadArea.addEventListener("click", () => fileInput.click());
uploadArea.addEventListener("dragover", (e) => e.preventDefault());
uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

// Drag and Drop functionality
uploadVendorArea.addEventListener("click", () => VendorfileInput.click());
uploadVendorArea.addEventListener("dragover", (e) => e.preventDefault());
uploadVendorArea.addEventListener("drop", (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleVendorFile(file);
});

uploadEmployeeArea.addEventListener("click", () => EmployeefileInput.click());
uploadEmployeeArea.addEventListener("dragover", (e) => e.preventDefault());
uploadEmployeeArea.addEventListener("drop", (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleEmployeeFile(file);
});

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    const fileName = fileInput.files[0].name;
    document.getElementById("mytext").value = "Uploaded Filename :- " + fileName;
    handleFile(file);
});

VendorfileInput.addEventListener("change", () => {
    const file = VendorfileInput.files[0];
    const fileName = VendorfileInput.files[0].name;
    document.getElementById("myVendortext").value = "Uploaded Filename :- " + fileName;
    handleVendorFile(file);
});

EmployeefileInput.addEventListener("change", () => {
    const file = EmployeefileInput.files[0];
    const fileName = EmployeefileInput.files[0].name;
    document.getElementById("myEmployeetext").value = "Uploaded Filename :- " + fileName;
    handleEmployeeFile(file);
});

function handleFile(file) {
    if (file && (file.name.endsWith(".csv") || file.name.endsWith(".xlsx"))) {
        previewContainer.style.display = "block";
        if (file.name.endsWith(".csv")) {
            readCSVFile(file);
        } else if (file.name.endsWith(".xlsx")) {
            readXLSXFile(file);
        }
    } else {
        alert("Please upload a valid CSV or XLSX file.");
    }
}

function handleVendorFile(file) {
    if (file && (file.name.endsWith(".csv") || file.name.endsWith(".xlsx"))) {
        previewVendorContainer.style.display = "block";
        if (file.name.endsWith(".csv")) {
            readVendorCSVFile(file);
        } else if (file.name.endsWith(".xlsx")) {
            readVendorXLSXFile(file);
        }
    } else {
        alert("Please upload a valid CSV or XLSX file.");
    }
}

function handleEmployeeFile(file) {
    if (file && (file.name.endsWith(".csv") || file.name.endsWith(".xlsx"))) {
        previewEmployeeContainer.style.display = "block";
        if (file.name.endsWith(".csv")) {
            readEmployeeCSVFile(file);
        } else if (file.name.endsWith(".xlsx")) {
            readEmployeeXLSXFile(file);
        }
    } else {
        alert("Please upload a valid CSV or XLSX file.");
    }
}

function readCSVFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const rawRows = e.target.result.split("\n");

        // Calculate the maximum number of columns in advance
        const maxCols = Math.max(...rawRows.map(row => row.split(",").length));

        const rows = rawRows.map(row => {
            // Split by comma and trim whitespace
            let cells = row.split(",").map(cell => cell.trim());

            // Normalize row length to match the longest row
            while (cells.length < maxCols) {
                cells.push(""); // Fill with empty strings if fewer columns
            }

            return cells;
        });

        displayPreview(rows);
    };
    reader.readAsText(file);
}

function readVendorCSVFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const rawRows = e.target.result.split("\n");

        // Calculate the maximum number of columns in advance
        const maxCols = Math.max(...rawRows.map(row => row.split(",").length));

        const rows = rawRows.map(row => {
            // Split by comma and trim whitespace
            let cells = row.split(",").map(cell => cell.trim());

            // Normalize row length to match the longest row
            while (cells.length < maxCols) {
                cells.push(""); // Fill with empty strings if fewer columns
            }

            return cells;
        });

        displayVendorPreview(rows);
    };
    reader.readAsText(file);
}

function readEmployeeCSVFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const rawRows = e.target.result.split("\n");

        // Calculate the maximum number of columns in advance
        const maxCols = Math.max(...rawRows.map(row => row.split(",").length));

        const rows = rawRows.map(row => {
            // Split by comma and trim whitespace
            let cells = row.split(",").map(cell => cell.trim());

            // Normalize row length to match the longest row
            while (cells.length < maxCols) {
                cells.push(""); // Fill with empty strings if fewer columns
            }

            return cells;
        });

        displayEmployeePreview(rows);
    };
    reader.readAsText(file);
}

function readXLSXFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        
        // Convert sheet to 2D array with empty cells included
        let rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: "" });

        // Ensure each row has the same length by padding with empty strings
        const maxCols = Math.max(...rows.map(row => row.length));
        rows = rows.map(row => {
            while (row.length < maxCols) {
                row.push(""); // Fill with empty strings if fewer columns
            }
            return row;
        });

        displayPreview(rows);
    };
    reader.readAsArrayBuffer(file);
}

function readVendorXLSXFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        
        // Convert sheet to 2D array with empty cells included
        let rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: "" });

        // Ensure each row has the same length by padding with empty strings
        const maxCols = Math.max(...rows.map(row => row.length));
        rows = rows.map(row => {
            while (row.length < maxCols) {
                row.push(""); // Fill with empty strings if fewer columns
            }
            return row;
        });

        displayVendorPreview(rows);
    };
    reader.readAsArrayBuffer(file);
}

function readEmployeeXLSXFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        
        // Convert sheet to 2D array with empty cells included
        let rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: "" });

        // Ensure each row has the same length by padding with empty strings
        const maxCols = Math.max(...rows.map(row => row.length));
        rows = rows.map(row => {
            while (row.length < maxCols) {
                row.push(""); // Fill with empty strings if fewer columns
            }
            return row;
        });

        displayEmployeePreview(rows);
    };
    reader.readAsArrayBuffer(file);
}

function displayPreview(rows) {
    clearPreview();
    
    // Limit preview to the first 10 rows (including header)
    const previewRows = rows.slice(0, 10);

    previewRows.forEach((row, i) => {
        const tr = document.createElement("tr");

        // Create a new cell for the Sr. No. (index + 1)
        const srNoCell = document.createElement(i === 0 ? "th" : "td");
        srNoCell.innerHTML = i === 0 ? "Sr. No." : i; // Add header for Sr. No. and display index for other rows
        tr.appendChild(srNoCell); // Append the Sr. No. cell to the row  
        
        row.forEach(cell => {
            const cellElem = i === 0 ? document.createElement("th") : document.createElement("td");
            
            // Set cell content to a non-breaking space if it's empty, ensuring alignment
            cellElem.innerHTML = cell ? cell : "&nbsp;";
            
            tr.appendChild(cellElem);
        });
        
        filePreview.appendChild(tr);
    });
}

function displayVendorPreview(rows) {
    clearVendorPreview();
    
    // Limit preview to the first 10 rows (including header)
    const previewRows = rows.slice(0, 10);

    previewRows.forEach((row, i) => {
        const tr = document.createElement("tr");
        
        row.forEach(cell => {
            const cellElem = document.createElement("td");
            
            // Set cell content to a non-breaking space if it's empty, ensuring alignment
            cellElem.innerHTML = cell ? cell : "&nbsp;";
            
            tr.appendChild(cellElem);
        });
        
        fileVendorPreview.appendChild(tr);
    });
}

function displayEmployeePreview(rows) {
    clearEmployeePreview();
    
    // Limit preview to the first 10 rows (including header)
    const previewRows = rows.slice(0, 10);

    previewRows.forEach((row, i) => {
        const tr = document.createElement("tr");
        
        row.forEach(cell => {
            const cellElem = document.createElement("td");
            
            // Set cell content to a non-breaking space if it's empty, ensuring alignment
            cellElem.innerHTML = cell ? cell : "&nbsp;";
            
            tr.appendChild(cellElem);
        });
        
        fileEmployeePreview.appendChild(tr);
    });
}


// Function to enable inline editing for a row
function editRow(button) {
    let row = button.closest("tr");
    row.querySelectorAll(".editable-cell").forEach((cell, index, cells) => {
        let cellType = cell.getAttribute("data-type");
        let currentValue = cell.textContent.trim();
        
        if (cellType === 'checkbox1') {
            // Create the dropdown with the correct option selected
            cell.innerHTML = `<select class="form-control form-control-sm">
                <option value="No" ${currentValue === 'No' ? 'selected' : ''}>No</option>
                <option value="Yes" ${currentValue === 'Yes' ? 'selected' : ''}>Yes</option>
            </select>`;

            // Add onchange listener to enable/disable and clear next cell if toggled to False
            const checkboxSelect = cell.querySelector("select");

            checkboxSelect.onchange = function () {
                // Get the cell right after the checkbox cell
                let nextCell = cells[index + 1];
                if (nextCell) {
                    let nextCellInput = nextCell.querySelector("input");
                    if (checkboxSelect.value === 'Yes') {
                        nextCell.classList.remove("disabled-cell");
                        if (nextCellInput) {
                            nextCellInput.disabled = false;
                        }
                    } else {
                        nextCell.classList.add("disabled-cell");
                        if (nextCellInput) {
                            nextCellInput.value = ''; // Clear the value
                            nextCellInput.disabled = true;
                        }
                    }
                }
            };

            // Trigger the onchange event initially to set the state
            checkboxSelect.onchange();
        } 
        else if(cellType === 'checkbox2') {
            // Create the dropdown with the correct option selected
            cell.innerHTML = `<select class="form-control form-control-sm">
                <option value="No" ${currentValue === 'No' ? 'selected' : ''}>No</option>
                <option value="Yes" ${currentValue === 'Yes' ? 'selected' : ''}>Yes</option>
            </select>`;

            // Add onchange listener to enable/disable and clear next cell if toggled to False
            const checkboxSelect = cell.querySelector("select");

            checkboxSelect.onchange = function () {
                // Get the cell right after the checkbox cell
                let nextCell = cells[index + 1];
                let nexttonextCell = cells[index + 2];
                if (nextCell) {
                    let nextCellInput = nextCell.querySelector("input");
                    let nexttonextCellInput = nexttonextCell.querySelector("input");
                    if (checkboxSelect.value === 'Yes') {
                        nextCell.classList.remove("disabled-cell");
                        nexttonextCell.classList.remove("disabled-cell");
                        if (nextCellInput) {
                            nextCellInput.disabled = false;
                            nexttonextCellInput.disabled = false;
                        }
                    } else {
                        nextCell.classList.add("disabled-cell");
                        nexttonextCell.classList.add("disabled-cell");
                        if (nextCellInput) {
                            nextCellInput.value = ''; // Clear the value
                            nexttonextCellInput.value = ''; // Clear the value
                            nextCellInput.disabled = true;
                            nexttonextCellInput.disabled = true;
                        }
                    }
                }
            };

            // Trigger the onchange event initially to set the state
            checkboxSelect.onchange();
        }
        else {
            cell.innerHTML = `<input type="${cellType}" value="${currentValue}" class="form-control form-control-sm" required>`;
        }
    });
    
    row.querySelector(".save-btn").classList.remove("d-none");
    row.querySelector(".edit-btn").classList.add("d-none");
    row.querySelector(".remove-btn").classList.add("d-none");
}


// Function to save edited values
function saveRow(button) {
    let row = button.closest("tr");
    row.querySelectorAll(".editable-cell").forEach(cell => {
        let input = cell.querySelector("input");
        let select = cell.querySelector("select");
        if (input) {
            cell.textContent = input.value;
        }
        if (select) {
            cell.textContent = select.value;
        }
    });
    row.querySelector(".save-btn").classList.add("d-none");
    row.querySelector(".edit-btn").classList.remove("d-none");
    row.querySelector(".remove-btn").classList.remove("d-none");
}

// Function to remove a row
function removeRow(button) {
    let row = button.closest("tr");
    row.remove();
}

function collectTableData() {
    const tableData = [];
    const rows = document.querySelectorAll("table tbody tr");
    // console.log(rows)
    const column = ['location', 'address', 'direct', 'noOfDirect', 'vendor', 'noOfVendor', 'total'];

    rows.forEach(row => {
        let rowData = {};
        let i = 0; // Initialize index for columns

        row.querySelectorAll(".editable-cell").forEach(cell => {
            let key = column[i]; // Use a unique key for each cell
            rowData[key] = cell.textContent.trim(); // Capture the cell's text content
            i++; // Increment the column index
        });

        if(rowData['location']){
            tableData.push(rowData); // Add the row data to the table data array
        }
        
    });
    
    return tableData;
}

document.querySelector('.download-button').addEventListener('click', function() {
    window.location.href = '/download-sample/';
});

// EXCEL VENDOR DETAILS JS


const closeExcelVendore = document.getElementById("close-vendore");
const closeExcelEmployeee = document.getElementById("close-employeee");

function closeExcelVendor(){
    excelVendorModal.style.display = "none"
}

function closeExcelEmployeer(){
    excelEmployeeModal.style.display = "none"
}

const excelVendorModal = document.getElementById("excelVendorModal")
const excelVendorBtn = document.getElementById("excelVendorBtn")

const excelEmployeeModal = document.getElementById("excelEmployeeModal")
const excelEmployeeBtn = document.getElementById("excelEmployeeBtn")

excelVendorBtn.onclick = () => {
    excelVendorModal.style.display = "block";
    previewVendorContainer.style.display = "none"
}

excelEmployeeBtn.onclick = () => {
    excelEmployeeModal.style.display = "block";
    previewEmployeeContainer.style.display = "none"
}

closeExcelVendore.onclick = () => {  closeExcelVendor() };

closeExcelEmployeee.onclick = () => {  closeExcelEmployeer() };

document.querySelector('.download-vendor-button').addEventListener('click', function() {
    window.location.href = '/download-vendor-sample/';
});

document.querySelector('.download-employee-button').addEventListener('click', function() {
    window.location.href = '/download-employee-sample/';
});

//MANUAL VENDOR DETAILS JS

function closeVendorModal(){
    manualVendorModal.style.display = "none";
    
}

const manualVendorModal = document.getElementById("manualVendorModal");
const manualVendorBtn = document.getElementById("manualVendorBtn");
const closeManualVendor = document.getElementById("close-vendor");

    manualVendorBtn.onclick = () => {

        const tableBodies = document.querySelectorAll(`#bootstrapVendordatatable tbody`);
        tableBodies.forEach(tbody => tbody.innerHTML = '');    

        var result = "";
        $.ajax({
            url: `/info/?_=${new Date().getTime()}`,
            type: 'GET',
            async: false,
            dataType: 'json',  // Expect a JSON response
            cache: false,      // Prevent caching in production
            headers: {
                'x-requested-with-vendor-data': 'vendor-data'
            },
            success: function(response) {
                result = response.locations_with_vendors;
            },
            error: function(xhr, errmsg, err) {
                console.error("Error fetching vendor data:", errmsg);
            }
        });
        
        // console.log(result);
    
        manualVendorModal.style.display = "block";
        const tablediv = document.querySelector('#table-content') 

        tablediv.innerHTML = ""
    
        for (let j = 0; j < result.length; j++) {
            const location_name = result[j][0];
            const vendor_details = result[j][1].length;

            if (tablediv){
                const table = document.createElement("table");
                table.classList.add("vendor-table");
                table.classList.add("table");
                table.classList.add("table-striped");
                table.classList.add("table-bordered");
                table.classList.add("text-center");

                // Create the table header section
                const thead = document.createElement("thead");

                thead.classList.add("thead-dark")

                // First row for location name
                const locationRow = document.createElement("tr");
                const locationHeader = document.createElement("th");
                locationHeader.colSpan = 14;
                locationHeader.classList.add("location-header");
                locationHeader.innerText = `LOCATION ${j + 1}: ${location_name}`;
                locationRow.appendChild(locationHeader);

                // Second row for column headers
                const headerRow = document.createElement("tr");
                headerRow.classList.add("header-row");

                const headers = [
                    "SR. NO", "VENDOR NAME", "VENDOR'S MYPOSH UID",
                    "VENDOR'S COMMUNICATION ADDRESS<span style='color: red;'>*</span>",
                    "MOBILE NUMBER<span style='color: red;'>*</span>",
                    "EMAIL ID<span style='color: red;'>*</span>",
                    "NATURE OF SERVICE", "CONTACT PERSON NAME<span style='color: red;'>*</span>",
                    "CONTACT PERSON MOBILE NO<span style='color: red;'>*</span>",
                    "CONTACT PERSON EMAIL ID<span style='color: red;'>*</span>",
                    "CONTRACT COMMENCEMENT DATE", "CONTRACT EXPIRY DATE",
                    "MAX NUMBER OF EMPLOYEES DEPLOYED", "Actions"
                ];

                // Create each header cell and append to header row
                headers.forEach(headerText => {
                    const th = document.createElement("th");
                    th.innerHTML = headerText;  // Use innerHTML to include HTML tags
                    headerRow.appendChild(th);
                });

                // Append the location and header rows to the table head
                thead.appendChild(locationRow);
                thead.appendChild(headerRow);
                table.appendChild(thead);

                // Create the table body
                const tbody = document.createElement("tbody");
                const locationNameList = location_name.split(" ")

                tbody.classList.add(locationNameList.join("-"));  // Set class dynamically based on location
                
                if (vendor_details > 0){
    
                    for (let i = 0; i < vendor_details; i++) {
        
                    // Check if tbody exists
                    if (tbody) {
                        const row = document.createElement("tr");
        
                        row.innerHTML = `
                            <td>${i + 1}</td>
                            <td data-type="text" class="editable-vendor-cell"></td>
                            <td data-type="text" class="editable-vendor-cell"></td>
                            <td data-type="text" class="editable-vendor-cell"></td>
                            <td data-type="numeric" class="editable-vendor-cell"></td>
                            <td data-type="email" class="editable-vendor-cell"></td>
                            <td data-type="text" class="editable-vendor-cell"></td>
                            <td data-type="text" class="editable-vendor-cell"></td>
                            <td data-type="numeric" class="editable-vendor-cell"></td>
                            <td data-type="email" class="editable-vendor-cell"></td>
                            <td data-type="date" class="editable-vendor-cell"></td>
                            <td data-type="date" class="editable-vendor-cell"></td>
                            <td data-type="number" class="editable-vendor-cell"></td>
                            <td class="action_buttons">
                                <button class="btn btn-primary btn-sm save-btn d-none" onclick="saveVendorRow(this)">Save</button>
                                <button class="btn btn-secondary btn-sm edit-btn" onclick="editVendorRow(this)">Edit</button>
                            </td>
                        `;
        
                        tbody.appendChild(row);

                        } 
                    }
                }else{
                if (tbody) {
                    const row = document.createElement("tr");
                    row.innerHTML = `<td colspan="14" class="text-center">No vendors available for this location</td>`
                    tbody.appendChild(row);
                }
            }
            // Append the table body to the table
            table.appendChild(tbody);
            const br = document.createElement("br");
            table.appendChild(br)
            tablediv.appendChild(table);
        }

    }
};

// Function to enable inline editing for a vendor row
function editVendorRow(button) {
    let row = button.closest("tr");
    row.querySelectorAll(".editable-vendor-cell").forEach((cell, index, cells) => {
        let cellType = cell.getAttribute("data-type");
        let currentValue = cell.textContent.trim();

        if (cellType === "numeric"){
            cell.innerHTML = `<input type="number" value="${currentValue}" class="form-control form-control-sm numeric">`;
        }
        else{
            cell.innerHTML = `<input type="${cellType}" value="${currentValue}" class="form-control form-control-sm">`;
        }
        
        
    });
    
    row.querySelector(".save-btn").classList.remove("d-none");
    row.querySelector(".edit-btn").classList.add("d-none");
}


// Function to save edited values
function saveVendorRow(button) {
    let row = button.closest("tr");
    row.querySelectorAll(".editable-vendor-cell").forEach(cell => {
        let input = cell.querySelector("input");
        if (input) {
            cell.textContent = input.value;
        }
    });
    row.querySelector(".save-btn").classList.add("d-none");
    row.querySelector(".edit-btn").classList.remove("d-none");
}


closeManualVendor.onclick = () => {  closeVendorModal() };



function collectVendorTableData() {
    const tableData = {}; // Main object to hold data by location_name
    const location_headers = document.querySelectorAll(".location-header");

    location_headers.forEach(location => {
        const location_name = location.textContent.split(":")[1].trim(); // Extract location name
        const locationNameList = location_name.split(" ")
        const tbodyClass = locationNameList.join("-");       
        
        // Initialize an array for each location_name to store its rows
        if (!tableData[location_name]) {
            tableData[location_name] = [];
        }

        // Select rows within the current location's tbody
        const rows = document.querySelectorAll(`tbody.${tbodyClass} tr`);
        
        const columns = ['vendorName', 'myposhID', 'commAddress', 
            'mobile', 'email', 'natureOfService', 'contactName',
            'contactMobile', 'contactEmail', 'contractStart', 'contractEnd', "maxEmp"];

        rows.forEach(row => {
            let rowData = {}; // Initialize an object to store cell data for this row
            let isEmpty = true; // Flag to track if all values are empty
            let i = 0; // Initialize index for columns

            row.querySelectorAll(".editable-vendor-cell").forEach(cell => {
                const key = columns[i]; // Use the corresponding key from columns
                const value = cell.textContent.trim();
                rowData[key] = value;

                if (value) {
                    isEmpty = false; // Set flag to false if there's any non-empty value
                }
                i++; // Move to the next column
            });

            // Only add non-empty rowData to the current location's array
            if (!isEmpty) {
                tableData[location_name].push(rowData);
            }
        });

        // Remove the location from tableData if it has only empty entries
        if (tableData[location_name].length === 0) {
            delete tableData[location_name];
        }
    });

    // console.log(tableData);
    return tableData;
}

//MANUAL EMPLOYEE DETAILS JS

function closeEmployeeModal(){
    manualEmployeeModal.style.display = "none";
    
}

const manualEmployeeModal = document.getElementById("manualEmployeeModal");
const manualEmployeeBtn = document.getElementById("manualEmployeeBtn");
const closeManualEmployee = document.getElementById("close-employee");

closeManualEmployee.onclick = () => {  closeEmployeeModal() };


manualEmployeeBtn.onclick = () => {
    manualEmployeeModal.style.display = "block";

    var data = "";
    $.ajax({
        url: `/info/?_=${new Date().getTime()}`,
        type: 'GET',
        async: false,
        dataType: 'json',  // Expect a JSON response
        cache: false,      // Prevent caching in production
        headers: {
            'x-requested-with-employee-data': 'employee-data'
        },
        success: function(response) {
            data = response.result;
        },
        error: function(xhr, errmsg, err) {
            console.error("Error fetching vendor data:", errmsg);
        }
    });

    // console.log(data)
    const tbody = document.querySelector("#bootstrapdatatableEmp tbody");

    // Clear any existing rows in the tbody
    tbody.innerHTML = '';
    let count = 0;

    // Iterate over each location in the data object
    for (const locationName in data) {
        const locationData = data[locationName];
        
        // console.log(locationData)
        // Add rows for Direct Employees if applicable
        if (locationData['Direct Employee'] > 0) {
            for (let j = 0; j < locationData['Direct Employee']; j++) {
                const directEmployeeRow = document.createElement('tr');
                directEmployeeRow.innerHTML = `
                    <td>${count + 1}</td>
                    <td>${locationName}</td>
                    <td>DIRECT</td>
                    <td></td>
                    <td data-type="text" class="editable-employee-cell"></td>
                    <td data-type="text" class="editable-employee-cell"></td>
                    <td data-type="select" class="editable-employee-cell"></td>
                    <td data-type="date" class="editable-employee-cell"></td>
                    <td data-type="numeric" class="editable-employee-cell"></td>
                    <td data-type="text" class="editable-employee-cell"></td>
                    <td class="action_buttons">
                        <button class="btn btn-primary btn-sm save-btn d-none" onclick="saveEmployeeRow(this)">Save</button>
                        <button class="btn btn-secondary btn-sm edit-btn" onclick="editEmployeeRow(this)">Edit</button>
                    </td>
                `;
                tbody.appendChild(directEmployeeRow);
                count++;
            }
        }
    
        // Add rows for each Vendor with Max Employees
        if (locationData['Vendors'].length > 0) {
            locationData['Vendors'].forEach(vendor => {
                for (let j = 0; j < vendor['Max Employees']; j++) {    
                    const vendorRow = document.createElement('tr');
                    vendorRow.innerHTML = `
                        <td>${count + 1}</td>
                        <td>${locationName}</td>
                        <td>INDIRECT</td>
                        <td>${vendor['Vendor Name']}</td>
                        <td data-type="text" class="editable-employee-cell"></td>
                        <td data-type="text" class="editable-employee-cell"></td>
                        <td data-type="select" class="editable-employee-cell"></td>
                        <td data-type="date" class="editable-employee-cell"></td>
                        <td data-type="numeric" class="editable-employee-cell"></td>
                        <td data-type="text" class="editable-employee-cell"></td>
                        <td class="action_buttons">
                            <button class="btn btn-primary btn-sm save-btn d-none" onclick="saveEmployeeRow(this)">Save</button>
                            <button class="btn btn-secondary btn-sm edit-btn" onclick="editEmployeeRow(this)">Edit</button>
                        </td>
                    `;
                    tbody.appendChild(vendorRow);
                    count++;
                }
            });
        }
    }
    
};


// Function to enable inline editing for a vendor row
function editEmployeeRow(button) {
    let row = button.closest("tr");
    row.querySelectorAll(".editable-employee-cell").forEach((cell, index, cells) => {
        let cellType = cell.getAttribute("data-type");
        let currentValue = cell.textContent.trim();

        if (cellType === "numeric"){
            cell.innerHTML = `<input type="number" value="${currentValue}" class="form-control form-control-sm numeric">`;
        }
        else if(cellType === "select"){
        cell.innerHTML = `<select class="form-control form-control-sm">
            <option value="Male" ${currentValue === 'Male' ? 'selected' : ''}>Male</option>
            <option value="Female" ${currentValue === 'Female' ? 'selected' : ''}>Female</option>
            <option value="Other" ${currentValue === 'Other' ? 'selected' : ''}>Other</option>
        </select>`;
        }
        else{
            cell.innerHTML = `<input type="${cellType}" value="${currentValue}" class="form-control form-control-sm">`;
        }
        
        
    });
    
    row.querySelector(".save-btn").classList.remove("d-none");
    row.querySelector(".edit-btn").classList.add("d-none");
}

function saveEmployeeRow(button) {
    let row = button.closest("tr");
    row.querySelectorAll(".editable-employee-cell").forEach(cell => {
        let input = cell.querySelector("input");
        let select = cell.querySelector("select");
        if (select) {
            cell.textContent = select.value;
        }
        if (input) {
            cell.textContent = input.value;
        }
    });
    row.querySelector(".save-btn").classList.add("d-none");
    row.querySelector(".edit-btn").classList.remove("d-none");
}

function collectEmployeeTableData() {

    const tableData = [];
    const rows = document.querySelectorAll("#bootstrapdatatableEmp tbody tr");

    // Loop through each row in the table
    rows.forEach(row => {
        const rowData = {};
        const cells = row.querySelectorAll('td');

        rowData['LOCATION'] = cells[1].innerText;
        rowData['NATURE OF EMPLOYMENT (DIRECT / INDIRECT)'] = cells[2].innerText; // DIRECT or INDIRECT
        rowData['VENDOR'] = cells[3].innerText;  // Empty for DIRECT

        rowData['NAME OF EMPLOYEE'] = cells[4].innerText; // Replace 'Field1' with actual field name
        rowData['MIDDLE NAME'] = cells[5].innerText;
        rowData['GENDER'] = cells[6].innerText;
        rowData['DATE OF JOINING'] = cells[7].innerText;
        rowData['MOBILE NUMBER'] = cells[8].innerText;
        rowData['EMAIL ID'] = cells[9].innerText;

        // Add the row data to the tableData array
        tableData.push(rowData);
    });
    // console.log(tableData)
    return tableData;
}

$('#manual-submission').on('click', function(event) {
    event.preventDefault();

    const tableData = collectTableData();
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  // Correct CSRF token selector

    // Send AJAX POST request to update certification details
    $.ajax({
        url: '/manual-data/',  // Use your endpoint URL here
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken   // Correct CSRF header
        },
        contentType: 'application/json',  // Set content type for JSON data
        data: JSON.stringify({ tableData: tableData }),
        success: function(response) {
            // Handle success (e.g., close modal, show success message)
            const manualModal = document.getElementById("manualModal");
            manualModal.style.display = "none";
            // location.reload();  // Reload the page to see the changes
            // console.log(response)
            if(response['status'] === 'success'){
                document.getElementById("message-success").style.display = "block";
                document.getElementById("nextstep2").hidden = false;
                document.getElementById("optionBtn").hidden = true;
                document.getElementById("countloc").disabled = true;

            }
        },
        error: function(xhr, errmsg, err) {
            // Handle error (e.g., show error message)
            console.log("Error:", errmsg);
        }
    });
});


$('#uploadButton').on('click', function(event) {
    event.preventDefault();
    
    // Get the selected file
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0]; // Get the first file
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); 
    
    if (file) {
        const formData = new FormData();
        formData.append('file', file); // Append the file to FormData

        // Send AJAX POST request to upload the CSV file
        $.ajax({
            url: '/upload-csv/', // Your Django URL for handling the file upload
            type: 'POST',
            processData: false, // Prevent jQuery from automatically processing the data
            contentType: false, // Set content type to false to let jQuery set it
            headers: {
                'X-CSRFToken': csrfToken  // Get CSRF token from cookies
            },
            data: formData,
            success: function(response) {
                // console.log('File uploaded successfully:', response);
                const excelModal = document.getElementById("excelModal");
                excelModal.style.display = "none";
                if(response['status'] === 'success'){
                    document.getElementById("message-success").style.display = "block";
                    document.getElementById("nextstep2").hidden = false
                    document.getElementById("optionBtn").hidden = true
                    document.getElementById("countloc").disabled = true
                }
                // Handle success (e.g., close modal, show success message)
            },
            error: function(xhr, errmsg, err) {
                console.error('Error uploading file:', errmsg);
                // Handle error (e.g., show error message)
            }
        });
    }
});

$('#uploadVendorButton').on('click', function(event) {
    event.preventDefault();
    
    // Get the selected file
    const fileInput = document.getElementById('VendorfileInput');
    const file = fileInput.files[0]; // Get the first file
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); 
    
    if (file) {
        const formData = new FormData();
        formData.append('file', file); // Append the file to FormData

        // Send AJAX POST request to upload the CSV file
        $.ajax({
            url: '/upload-vendor-csv/', // Your Django URL for handling the file upload
            type: 'POST',
            processData: false, // Prevent jQuery from automatically processing the data
            contentType: false, // Set content type to false to let jQuery set it
            headers: {
                'X-CSRFToken': csrfToken  // Get CSRF token from cookies
            },
            data: formData,
            success: function(response) {
                console.log('File uploaded successfully:', response);
                const excelVendorModal = document.getElementById("excelVendorModal");
                excelVendorModal.style.display = "none";
                if(response['status'] === 'success'){
                    document.getElementById("message-vendor-success").style.display = "block";
                    document.getElementById("nextstep3").hidden = false;
                    document.getElementById("manualVendorBtn").hidden = true;
                    document.getElementById("excelVendorBtn").hidden= true;
    
                    }
                // Handle success (e.g., close modal, show success message)
            },
            error: function(xhr, errmsg, err) {
                console.error('Error uploading file:', errmsg);
                // Handle error (e.g., show error message)
            }
        });
    }
});


$('#uploadEmployeeButton').on('click', function(event) {
    event.preventDefault();

    $('#loading-screen').show();

    // Get the selected file
    const fileInput = document.getElementById('EmployeefileInput');
    const file = fileInput.files[0]; // Get the first file
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); 

    if (file) {
        const formData = new FormData();
        formData.append('file', file); // Append the file to FormData

        // Send AJAX POST request to upload the CSV file
        $.ajax({
            url: '/info/', // Your Django URL for handling the file upload
            type: 'POST',
            processData: false, // Prevent jQuery from automatically processing the data
            contentType: false, // Set content type to false to let jQuery set it
            headers: {
                'X-CSRFToken': csrfToken  // Get CSRF token from cookies
            },
            data: formData,
            success: function(response) {
                if(response['status'] === 'success'){
                    $('#loading-screen').hide();
                    // Handle success (e.g., close modal, show success message)
                    const excelEmployeeModal = document.getElementById("excelEmployeeModal");
                    excelEmployeeModal.style.display = "none";
                    // location.reload();  // Reload the page to see the changes
                    // console.log(response)
                    if(response['status'] === 'success'){
                        // document.getElementById("message-employee-success").style.display = "block";
                        document.getElementById("manualEmployeeBtn").hidden = true;
                        document.getElementById("excelEmployeeBtn").hidden= true;
                        document.getElementById("lastbackbutton").hidden= true;
                        showVendorSuccessMessage()
                        // Delay redirect by 3 seconds (adjust if needed)
                        setTimeout(() => {
                            window.location = '/';
                        }, 3000);
    
                    }
                }
            },
            error: function(xhr, errmsg, err) {
                $('#loading-screen').hide();
                console.error('Error uploading file:', errmsg);
                // Handle error (e.g., show error message)
            }
        });
    }
});


//Manual-Vendor-Submission
$('#manual-vendor-submission').on('click', function(event) {
    event.preventDefault();

    const tableData = collectVendorTableData();
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  // Correct CSRF token selector

    // Send AJAX POST request to update certification details
    $.ajax({
        url: '/manual-vendor-data/',  // Use your endpoint URL here
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken   // Correct CSRF header
        },
        contentType: 'application/json',  // Set content type for JSON data
        data: JSON.stringify({ tableData: tableData }),
        success: function(response) {
            // Handle success (e.g., close modal, show success message)
            const manualVendorModal = document.getElementById("manualVendorModal");
            manualVendorModal.style.display = "none";
            // location.reload();  // Reload the page to see the changes
            // console.log(response)
            if(response['status'] === 'success'){
                document.getElementById("message-vendor-success").style.display = "block";
                document.getElementById("nextstep3").hidden = false;
                document.getElementById("manualVendorBtn").hidden = true;
                document.getElementById("excelVendorBtn").hidden= true;

            }
        },
        error: function(xhr, errmsg, err) {
            // Handle error (e.g., show error message)
            console.log("Error:", errmsg);
        }
    });
});

//Manual-Employee-Submission
$('#manual-employee-submission').on('click', function(event) {
    event.preventDefault();

    $('#loading-screen-manual').show();

    const tableData = collectEmployeeTableData();
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  // Correct CSRF token selector

    // Send AJAX POST request to update certification details
    $.ajax({
        url: '/info/',  // Use your endpoint URL here
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken   // Correct CSRF header
        },
        contentType: 'application/json',  // Set content type for JSON data
        data: JSON.stringify({ tableData: tableData }),
        success: function(response) {
            if(response['status'] === 'success'){
                // Handle success (e.g., close modal, show success message)
                $('#loading-screen-manual').hide();
                const manualEmployeeModal = document.getElementById("manualEmployeeModal");
                manualEmployeeModal.style.display = "none";
                // location.reload();  // Reload the page to see the changes
                // console.log(response)
                if(response['status'] === 'success'){
                    // document.getElementById("message-employee-success").style.display = "block";
                    document.getElementById("manualEmployeeBtn").hidden = true;
                    document.getElementById("excelEmployeeBtn").hidden= true;
                    document.getElementById("lastbackbutton").hidden= true;
                    showVendorSuccessMessage()
                    // Delay redirect by 3 seconds (adjust if needed)
                    setTimeout(() => {
                        window.location = '/';
                    }, 3000);

                }
            }
        },
        error: function(xhr, errmsg, err) {
            $('#loading-screen-manual').hide();
            // Handle error (e.g., show error message)
            console.log("Error:", errmsg);
        }
    });
});

function showVendorSuccessMessage() {
    const messageDiv = document.getElementById("message-employee-success");
    messageDiv.style.display = "block";
    messageDiv.style.opacity = '1'; // Fade in effect
    setTimeout(() => {
        messageDiv.style.opacity = '0'; // Fade out effect after 3 seconds
        setTimeout(() => {
            messageDiv.style.display = "none";
        }, 500); // Adjust delay for fade-out transition
    }, 3000); // Duration the message is visible
}

// LOADER
onload = () => {
    const load = document.getElementById('load')

    setTimeout(() => {
        load.style.display = 'none'
    }, 500)
}