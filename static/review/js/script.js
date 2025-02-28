// static/js/review.js
document.addEventListener("DOMContentLoaded", function() {
    const stars = document.querySelectorAll(".star-rating i");
    const ratingInput = document.getElementById("id_rating"); // Crispy auto-generates field ID
    const currentRating = parseInt(ratingInput.value, 10); // Get current rating value

    // Highlight stars based on existing rating
    if (!isNaN(currentRating)) {
        stars.forEach(star => {
            if (star.getAttribute("data-value") <= currentRating) {
                star.classList.add("selected");
            }
        });
    }

    // Add event listener for selecting new rating
    stars.forEach(star => {
        star.addEventListener("click", function() {
            let value = this.getAttribute("data-value");
            ratingInput.value = value;

            // Update star highlighting
            stars.forEach(s => {
                s.classList.remove("selected");
                if (s.getAttribute("data-value") <= value) {
                    s.classList.add("selected");
                }
            });
        });
    });
});
