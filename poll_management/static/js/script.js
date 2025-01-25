document.addEventListener("DOMContentLoaded", () => {
    const pollStatus = document.getElementById("poll-status").textContent.split(": ")[1].trim();

    const lockButton = document.getElementById("lock");
    const unlockButton = document.getElementById("unlock");

    //show or hide buttons based on poll status
    if (pollStatus === "active") {
        unlockButton.style.display = "none";
    } else if (pollStatus === "closed") {
        lockButton.style.display = "none";
    }
});