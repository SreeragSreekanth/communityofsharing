document.addEventListener("DOMContentLoaded", function () {
    let eventCount = localStorage.getItem('new_event_count');
    let announcementCount = localStorage.getItem('new_announcement_count');

    if (eventCount > 0) {
        document.getElementById("event-count").textContent = eventCount;
        document.getElementById("event-count").style.display = "inline-block";
    } else {
        document.getElementById("event-count").style.display = "none";
    }

    if (announcementCount > 0) {
        document.getElementById("announcement-count").textContent = announcementCount;
        document.getElementById("announcement-count").style.display = "inline-block";
    } else {
        document.getElementById("announcement-count").style.display = "none";
    }
});

function resetEventCount() {
    localStorage.setItem('new_event_count', 0);
    document.getElementById("event-count").style.display = "none";
}

function resetAnnouncementCount() {
    localStorage.setItem('new_announcement_count', 0);
    document.getElementById("announcement-count").style.display = "none";
}
