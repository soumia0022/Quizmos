document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("joinPollForm");
    const pollCodeInput = document.getElementById("pollCode");

    form.addEventListener("submit", function (event) {
        const pollCodeValue = pollCodeInput.value;
        const isValidLength = pollCodeValue.length === 6;
        const isNumeric = /^\d+$/.test(pollCodeValue);

        if (!isValidLength || !isNumeric) {
            event.preventDefault();
            alert("Please enter a valid 6-digit numeric poll code.");
        }
    });
});
