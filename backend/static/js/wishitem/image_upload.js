document.addEventListener("DOMContentLoaded", function () {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("id_picture");
    const preview = document.getElementById("preview");
    const plusSign = document.getElementById("plus-sign");
    const borderSign = document.getElementById("border-sign");
    const clearPreviewButton = document.getElementById("clear-preview-button");

    if (!dropZone || !fileInput || !preview || !plusSign || !borderSign || !clearPreviewButton) {
        console.error("Missing elements");
        return;
    }

    function updatePreview(file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.classList.remove("hidden");
            borderSign.classList.remove("hidden");
            plusSign.classList.add("hidden");
            clearPreviewButton.classList.remove("hidden");
        };
        reader.onerror = function (e) {
            console.error("FileReader error:", e);
        };
        reader.readAsDataURL(file);
        const clearCheckbox = document.querySelector('input[name="picture-clear"]');
        if (clearCheckbox) {
            clearCheckbox.checked = false;
        }
    }

    function resetPreview() {
        preview.src = "";
        preview.classList.add("hidden");
        borderSign.classList.add("hidden");
        plusSign.classList.remove("hidden");
        clearPreviewButton.classList.add("hidden");
        fileInput.value = "";
        const clearCheckbox = document.querySelector('input[name="picture-clear"]');
        if (clearCheckbox) {
            clearCheckbox.checked = true;
        }
    }

    // Обработка выбора файла вручную
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            updatePreview(fileInput.files[0]);
        } else {
            resetPreview();
        }
    });

    // Drag'n'Drop
    dropZone.addEventListener("dragover", function (e) {
        e.preventDefault();
    });

    dropZone.addEventListener("dragleave", function () {
    });

    dropZone.addEventListener("drop", function (e) {
        e.preventDefault();

        if (e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
            updatePreview(file);
        }
    });

    // Сделать зону кликабельной
    dropZone.addEventListener("click", function () {
        fileInput.click();
    });

    // Вставка из буфера обмена
    document.addEventListener("paste", function (e) {
        const items = e.clipboardData.items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf("image") !== -1) {
                const file = items[i].getAsFile();
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;
                updatePreview(file);
                break;
            }
        }
    });

    // Обработка кнопки "Удалить"
    clearPreviewButton.addEventListener("click", function () {
        resetPreview();
    });
});
