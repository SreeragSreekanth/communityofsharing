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

document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript file loaded successfully!");

    // Confirmation for Delete Item
    document.querySelectorAll(".delete-item").forEach(button => {
        button.addEventListener("click", function (event) {
            if (!confirm("Are you sure you want to delete this item? This action cannot be undone.")) {
                event.preventDefault();
            }
        });
    });

    // Confirmation for Borrow Request
    document.querySelectorAll(".request-borrow").forEach(button => {
        button.addEventListener("click", function (event) {
            if (!confirm("Are you sure you want to send a borrow request for this item?")) {
                event.preventDefault();
            }
        });
    });
});
