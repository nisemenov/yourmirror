document.addEventListener("DOMContentLoaded", function () {
    const reserveBtn = document.getElementById("reserve-button");
    const reserveModal = document.getElementById("reserve-modal");
    const closeBtn = document.getElementById("close-button");

    if (reserveBtn && reserveModal && closeBtn) {
        reserveBtn.addEventListener("click", () => {
            reserveModal.classList.remove("hidden");
        });

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
