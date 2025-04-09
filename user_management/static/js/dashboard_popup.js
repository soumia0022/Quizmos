
document.getElementById("confirmCreatePoll").addEventListener("click", function() {
    let button = this;
    let form = document.createElement("form");
    form.method = "POST";
    form.action = "";

    let csrfToken = document.createElement("input");
    csrfToken.type = "hidden";
    csrfToken.name = "csrfmiddlewaretoken";
    csrfToken.value = button.getAttribute("data-csrf-token");

    let titleInput = document.createElement("input");
    titleInput.type = "hidden";
    titleInput.name = "title";
    titleInput.value = button.getAttribute("data-suggested-title");

    let confirmedInput = document.createElement("input");
    confirmedInput.type = "hidden";
    confirmedInput.name = "confirmed";
    confirmedInput.value = "true";

    form.appendChild(csrfToken);
    form.appendChild(titleInput);
    form.appendChild(confirmedInput);
    document.body.appendChild(form);
    form.submit();
});

document.getElementById("cancelCreatePoll").addEventListener("click", function() {
    let button = this;
    let form = document.createElement("form");
    form.method = "POST";
    form.action = "";

    let csrfToken = document.createElement("input");
    csrfToken.type = "hidden";
    csrfToken.name = "csrfmiddlewaretoken";
    csrfToken.value = button.getAttribute("data-csrf-token");

    let cancelInput = document.createElement("input");
    cancelInput.type = "hidden";
    cancelInput.name = "cancelled";
    cancelInput.value = "true";

    form.appendChild(csrfToken);
    form.appendChild(cancelInput);
    document.body.appendChild(form);
    form.submit();
});
