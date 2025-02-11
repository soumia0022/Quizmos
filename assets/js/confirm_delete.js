document.addEventListener("DOMContentLoaded", function () {
    let deletePollId = null;

    document.querySelectorAll("button[onclick^='confirmDelete']").forEach(button => {
        button.addEventListener("click", function () {
            deletePollId = this.getAttribute("data-id");
            document.getElementById("custom-popup").style.display = "flex";
        });
    });

    document.getElementById("confirm-delete").addEventListener("click", function () {
        if (deletePollId) {
            document.getElementById(`delete-form-${deletePollId}`).submit();
        }
    });

    document.getElementById("cancel-delete").addEventListener("click", function () {
        document.getElementById("custom-popup").style.display = "none";
    });
});