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