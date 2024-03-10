document.addEventListener('DOMContentLoaded', function () {
    const educationList = document.getElementById('education-list');
    const skillsList = document.getElementById('skills-list')
    const addEducationBtn = document.getElementById('add-education-btn');
    const addSkillsBtn = document.getElementById('add-skills-btn');
    const saveEducationBtn = document.getElementById('saveEducationBtn');
    const saveSkillsBtn = document.getElementById('saveskillsBtn');

    const schoolInput = document.getElementById('schoolInput');
    const degreeInput = document.getElementById('degreeInput');
    const fieldOfStudyInput = document.getElementById('fieldOfStudyInput');
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    const gradeInput = document.getElementById('gradeInput');
    const descriptionInput = document.getElementById('descriptionInput');

    const skillsInput = document.getElementById('skillsInput');

    addEducationBtn.addEventListener('click', function () {
        $('#addEducationModal').modal('show');
    });

    addSkillsBtn.addEventListener('click', function () {
        $('#addskillsModal').modal('show');
    });

    saveSkillsBtn.addEventListener('click', function () {
        const newSkill = skillsInput.value.trim();

        if (newSkill){
            const existingSkillItem = skillsList.querySelector('.skill-editing');
            if (existingSkillItem ) {
                // Update the content of the existing list item
                const skillcardContent = existingSkillItem.querySelector('.skillcard-content');
                const skillleftSide = skillcardContent.querySelector('.skill-left-side');

                skillleftSide.innerHTML = `
                    <div class='skill_name'>${newSkill}</div>
                `;

                // Remove the 'editing' class
                existingSkillItem.classList.remove('skill-editing');
            } else {
                // Create a new list item if there is no existing one
                const skill_li = document.createElement('li');
                skill_li.className = 'skill-list-group-item';

                const skillcardContent = document.createElement('div');
                skillcardContent.className = 'skillcard-content';

                const skillleftSide = document.createElement('div');
                skillleftSide.className = 'skill-left-side';
                skillleftSide.innerHTML = `
                    <div class='skill_name'>${newSkill}</div>
                `;

                const editButton = document.createElement('button');
                editButton.className = 'btn btn-warning btn-sm mr-2';
                editButton.textContent = 'Edit';
                editButton.addEventListener('click', function () {
                    // Handle edit logic here
                    // You can open a modal for editing or perform any other action
                    skill_li.classList.add('skill-editing'); // Add 'editing' class for identification
                });

                const deleteButton = document.createElement('button');
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.textContent = 'Delete';
                deleteButton.addEventListener('click', function () {
                    // Handle delete logic here
                    // You can remove the list item from the education list
                    skill_li.remove();
                });

                skillcardContent.appendChild(skillleftSide);
                skill_li.appendChild(skillcardContent);
                skill_li.appendChild(editButton);
                skill_li.appendChild(deleteButton);
                skillsList.appendChild(skill_li);
            }

            // Close the modal
            $('#addskillsModal').modal('hide');

            // Clear the input fields
            skillsInput.value = '';
        }
        
    });

    skillsList.addEventListener('click', function (event) {
        const targetskill = event.target;

        if (targetskill.classList.contains('btn-warning')) {
            // Get the list item containing the edit button
            const skilllistItem = targetskill.closest('li');

            // Populate the modal with the current values
            const skillcardContent = skilllistItem.querySelector('.skillcard-content');
            const skillleftSide = skillcardContent.querySelector('.skill-left-side');

            skillsInput.value = skillleftSide.children[0].textContent;

            // Show the modal for editing
            $('#addskillsModal').modal('show');
        }
    });

    saveEducationBtn.addEventListener('click', function () {
        const newSchool = schoolInput.value.trim();
        const newDegree = degreeInput.value.trim();
        const newFieldOfStudy = fieldOfStudyInput.value.trim();
        const newStartDate = startDate.value.trim();
        const newEndDate = endDate.value.trim();
        const newGrade = gradeInput.value.trim();
        const newDescription = descriptionInput.value.trim();

        if (newSchool && newDegree && newFieldOfStudy) {
            // Check if there is an existing list item for editing
            const existingListItem = educationList.querySelector('.editing');

            if (existingListItem) {
                // Update the content of the existing list item
                const cardContent = existingListItem.querySelector('.card-content');
                const leftSide = cardContent.querySelector('.left-side');
                const rightSide = cardContent.querySelector('.right-side');

                leftSide.innerHTML = `
                    <div class='college_name'>${newSchool}</div>
                    <div class='degree'>${newDegree} - ${newFieldOfStudy}</div>
                    <div class='desc'>${newDescription}</div>
                `;

                rightSide.innerHTML = `
                    <div class='year'>${newStartDate} to ${newEndDate}</div>
                    <div class='grade'>Grade: ${newGrade}</div>
                `;

                // Remove the 'editing' class
                existingListItem.classList.remove('editing');
            } else {
                // Create a new list item if there is no existing one
                const li = document.createElement('li');
                li.className = 'list-group-item';

                const cardContent = document.createElement('div');
                cardContent.className = 'card-content';

                const leftSide = document.createElement('div');
                leftSide.className = 'left-side';
                leftSide.innerHTML = `
                    <div class='college_name'>${newSchool}</div>
                    <div class='degree'>${newDegree} - ${newFieldOfStudy}</div>
                    <div class='desc'>${newDescription}</div>
                `;

                const rightSide = document.createElement('div');
                rightSide.className = 'right-side';
                rightSide.innerHTML = `
                    <div class='year'>${newStartDate} to ${newEndDate}</div>
                    <div class='grade'>Grade: ${newGrade}</div>
                `;

                const editButton = document.createElement('button');
                editButton.className = 'btn btn-warning btn-sm mr-2';
                editButton.textContent = 'Edit';
                editButton.addEventListener('click', function () {
                    // Handle edit logic here
                    // You can open a modal for editing or perform any other action
                    li.classList.add('editing'); // Add 'editing' class for identification
                });

                const deleteButton = document.createElement('button');
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.textContent = 'Delete';
                deleteButton.addEventListener('click', function () {
                    // Handle delete logic here
                    // You can remove the list item from the education list
                    li.remove();
                });

                cardContent.appendChild(leftSide);
                cardContent.appendChild(rightSide);
                li.appendChild(cardContent);
                li.appendChild(editButton);
                li.appendChild(deleteButton);
                educationList.appendChild(li);
            }

            // Close the modal
            $('#addEducationModal').modal('hide');

            // Clear the input fields
            schoolInput.value = '';
            degreeInput.value = '';
            fieldOfStudyInput.value = '';
            startDate.value = '';
            endDate.value = '';
            gradeInput.value = '';
            descriptionInput.value = '';
        }
    });

    educationList.addEventListener('click', function (event) {
        const target = event.target;

        if (target.classList.contains('btn-warning')) {
            // Get the list item containing the edit button
            const listItem = target.closest('li');

            // Populate the modal with the current values
            const cardContent = listItem.querySelector('.card-content');
            const leftSide = cardContent.querySelector('.left-side');
            const rightSide = cardContent.querySelector('.right-side');

            schoolInput.value = leftSide.children[0].textContent;
            const degreeAndField = leftSide.children[1].textContent.split(' - ');
            degreeInput.value = degreeAndField[0];
            fieldOfStudyInput.value = degreeAndField[1];
            const dateRange = rightSide.children[0].textContent.split(' to ');
            startDate.value = dateRange[0];
            endDate.value = dateRange[1];
            gradeInput.value = rightSide.children[1].textContent.split(': ')[1];
            descriptionInput.value = leftSide.children[2].textContent;

            // Show the modal for editing
            $('#addEducationModal').modal('show');
        }
    });
});
