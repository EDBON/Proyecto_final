document.addEventListener('DOMContentLoaded', function() {
    // Get references to the DOM elements
    const fileInput = document.getElementById('{{ form.imagen.id_for_label }}');
    let profileImagePreview = document.getElementById('profile-image-preview'); // Use 'let' because it might be created
    const profileImageIcon = document.getElementById('profile-image-icon');
    const profilePicturePlaceholder = document.querySelector('.profile-picture-placeholder');
    const fileNameDisplay = document.getElementById('file-name-display'); // For accessibility

    // Check if the file input exists on the page
    if (fileInput) {
        // Add an event listener for when the file input's value changes
        fileInput.addEventListener('change', function() {
            // Check if a file was selected
            if (this.files && this.files[0]) {
                const selectedFile = this.files[0];
                const reader = new FileReader(); // Create a new FileReader object

                // Define what happens when the reader finishes loading the file
                reader.onload = function(e) {
                    // If an image preview element already exists, update its src
                    if (profileImagePreview) {
                        profileImagePreview.src = e.target.result;
                        profileImagePreview.style.display = 'block'; // Ensure it's visible
                    } else {
                        // If no image preview element exists (e.g., first upload)
                        // Create a new <img> element
                        profileImagePreview = document.createElement('img');
                        profileImagePreview.id = 'profile-image-preview';
                        profileImagePreview.classList.add('current-profile-image'); // Apply your existing styling class
                        profileImagePreview.alt = 'Profile Picture Preview';
                        
                        // Set the src to the base64 encoded image data
                        profileImagePreview.src = e.target.result;
                        
                        // Append the new image element to the placeholder
                        profilePicturePlaceholder.appendChild(profileImagePreview);
                    }

                    // Hide the camera icon if it's visible
                    if (profileImageIcon) {
                        profileImageIcon.style.display = 'none';
                    }
                    
                    // Update the hidden span for screen readers
                    fileNameDisplay.textContent = selectedFile.name;

                    // Remove any existing error messages for the image field (optional, but good UX)
                    const errorList = fileInput.closest('.form-group').querySelector('.errorlist');
                    if (errorList) {
                        errorList.innerHTML = ''; // Clear previous errors
                    }
                };

                // Read the selected file as a Data URL (base64 encoded string)
                reader.readAsDataURL(selectedFile);
            } else {
                // If no file is selected (e.g., user cancels the file dialog)
                if (profileImagePreview) {
                    profileImagePreview.src = ''; // Clear the image source
                    profileImagePreview.style.display = 'none'; // Hide the image
                }
                // Show the camera icon again
                if (profileImageIcon) {
                    profileImageIcon.style.display = 'block';
                }
                fileNameDisplay.textContent = 'Ningún archivo seleccionado';
            }
        });
    }
});