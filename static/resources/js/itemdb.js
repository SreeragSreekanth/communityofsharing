document.addEventListener("DOMContentLoaded", function () {
    console.log("JS Loaded 🚀"); // Debugging step 1

    // DELETE ITEM CONFIRMATION
    let deleteButton = document.querySelector(".delete-item");
    if (deleteButton) {
        deleteButton.addEventListener("click", function (event) {
            if (!confirm("Are you sure you want to delete this item? This action cannot be undone.")) {
                event.preventDefault();
            }
        });
    }

    // BORROW REQUEST CONFIRMATION (Fixed)
    let borrowForm = document.getElementById("borrow-request-form");
    if (borrowForm) {
        console.log("Borrow form found ✅"); // Debugging step 2

        borrowForm.addEventListener("submit", function (event) {
            let userConfirmed = confirm("Are you sure you want to request to borrow this item?");
            
            if (!userConfirmed) {
                event.preventDefault();
                console.log("Borrow request cancelled ❌"); // Debugging step 3
            } else {
                console.log("Borrow request submitted ✅"); // Debugging step 4
            }
        });
    } else {
        console.log("Borrow form NOT found ❌"); // Debugging step 5
    }
});
