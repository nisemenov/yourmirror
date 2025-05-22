document.addEventListener("DOMContentLoaded", function () {
    const reserveModal = document.getElementById("reserve-modal");
    const reserveText = document.getElementById("reserve-text");
    const sentText = document.getElementById("sent-text");
    const emailForm = document.getElementById("email-form");
    const closeBtn = document.getElementById("close-button");

    if (reserveModal && reserveText && sentText && emailForm && closeBtn) {
        reserveModal.classList.remove("hidden");
        reserveText.classList.add("hidden");
        sentText.classList.remove("hidden");
        emailForm.classList.add("hidden");

        closeBtn.addEventListener("click", () => {
            reserveModal.classList.add("hidden");
        });

        window.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                reserveModal.classList.add("hidden");
            }
        });

        reserveModal.addEventListener("click", (e) => {
            if (e.target === reserveModal) {
                reserveModal.classList.add("hidden");
            }
        });
    }
});
