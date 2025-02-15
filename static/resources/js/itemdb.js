document.addEventListener("DOMContentLoaded", function () {
    console.log("JS Loaded 🚀");

    // DELETE ITEM CONFIRMATION (Handles multiple delete buttons)
    document.querySelectorAll(".delete-item").forEach(button => {
        button.addEventListener("click", function (event) {
            if (!confirm("Are you sure you want to delete this item? This action cannot be undone.")) {
                event.preventDefault();
            } else {
                this.disabled = true; // Prevent multiple clicks
            }
        });
    });

    // BORROW REQUEST CONFIRMATION (Fix double alert issue)
    let borrowForm = document.getElementById("borrow-request-form");
    if (borrowForm && !borrowForm.dataset.listener) {  // Prevent duplicate event binding
        borrowForm.dataset.listener = "true";  // Mark as processed
        borrowForm.addEventListener("submit", function (event) {
            if (!confirm("Are you sure you want to request to borrow this item?")) {
                event.preventDefault();
            } else {
                borrowForm.querySelector("button[type='submit']").disabled = true; // Prevent multiple submits
            }
        });
    }
});
