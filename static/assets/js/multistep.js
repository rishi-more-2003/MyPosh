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
    
        // Example boolean values; replace these with your actual boolean values
        const isEditable1 = false; // Boolean for first condition
        const isEditable2 = false; // Boolean for second condition
    
        row.innerHTML = `
            <td>${i + 1}</td>
            <td data-type="text" class="editable-cell"></td>
            <td data-type="text" class="editable-cell"></td>
            <td data-type="checkbox" class="editable-cell"></td>
            <td data-type="number" class="editable-cell"></td>
            <td data-type="checkbox" class="editable-cell"></td>
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

// Drag and Drop functionality
uploadArea.addEventListener("click", () => fileInput.click());
uploadArea.addEventListener("dragover", (e) => e.preventDefault());
uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    const fileName = fileInput.files[0].name;
    document.getElementById("mytext").value = "Uploaded Filename :- " + fileName;
    handleFile(file);
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


// Function to enable inline editing for a row
function editRow(button) {
    let row = button.closest("tr");
    row.querySelectorAll(".editable-cell").forEach((cell, index, cells) => {
        let cellType = cell.getAttribute("data-type");
        let currentValue = cell.textContent.trim();
        
        if (cellType === 'checkbox') {
            // Create the dropdown with the correct option selected
            cell.innerHTML = `<select class="form-control form-control-sm">
                <option value="False" ${currentValue === 'False' ? 'selected' : ''}>False</option>
                <option value="True" ${currentValue === 'True' ? 'selected' : ''}>True</option>
            </select>`;

            // Add onchange listener to enable/disable and clear next cell if toggled to False
            const checkboxSelect = cell.querySelector("select");

            checkboxSelect.onchange = function () {
                // Get the cell right after the checkbox cell
                let nextCell = cells[index + 1];
                if (nextCell) {
                    let nextCellInput = nextCell.querySelector("input");
                    if (checkboxSelect.value === 'True') {
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
        } else {
            cell.innerHTML = `<input type="${cellType}" value="${currentValue}" class="form-control form-control-sm">`;
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
    const column = ['location', 'address', 'direct', 'noOfDirect', 'vendor', 'noOfVendor', 'total'];

    rows.forEach(row => {
        let rowData = {};
        let i = 0; // Initialize index for columns

        row.querySelectorAll(".editable-cell").forEach(cell => {
            let key = column[i]; // Use a unique key for each cell
            rowData[key] = cell.textContent.trim(); // Capture the cell's text content
            i++; // Increment the column index
        });

        tableData.push(rowData); // Add the row data to the table data array
    });

    return tableData;
}

document.querySelector('.download-button').addEventListener('click', function() {
    window.location.href = '/download-sample/';
});
