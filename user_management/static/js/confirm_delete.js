document.addEventListener("DOMContentLoaded", function () {
    let deletePollId = null;

    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function () {
            deletePollId = this.getAttribute("data-id");
            document.getElementById("custom-popup").style.display = "flex";
        });
    });

    const confirmBtn = document.getElementById("confirm-delete");
    if (confirmBtn) {
        confirmBtn.addEventListener("click", function () {
            if (deletePollId) {
                document.getElementById(`delete-form-${deletePollId}`).submit();
            }
        });
    }

    const cancelBtn = document.getElementById("cancel-delete");
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            document.getElementById("custom-popup").style.display = "none";
        });
    }
});
