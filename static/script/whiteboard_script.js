function getCurrentDateFormatted() {
    const date = new Date();
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    const month = monthNames[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();
    return `${month} ${day}, ${year}`;
}

function homePrePageLoad() {
    // Get the current date and display it in the p tag
    const currentDateElement = document.getElementById('currentDate');
    currentDateElement.textContent = getCurrentDateFormatted();
}

function changeTemplate(url) {
    window.location.href = url;
}