document.addEventListener('DOMContentLoaded', function () {
    // Find the "Add Photo" button by its ID
    const addButton = document.getElementById('add-photo');
    if (addButton) {
        addButton.addEventListener('click', function () {
            // Find the container for image fields
            const container = document.getElementById('image-fields');
            if (container) {
                // Create a new div for the image field
                const newField = document.createElement('div');
                newField.classList.add('mb-3');
                newField.innerHTML = '<input type="file" name="images" class="form-control">';
                container.appendChild(newField);
            }
        });
    }
});