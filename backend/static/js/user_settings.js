document.addEventListener("DOMContentLoaded", function () {
    const enableEdit = document.getElementById("enable-edit")
    const cancelEdit = document.getElementById("cancel-edit")
    const saveEdit = document.getElementById("save-edit")
    const form = document.querySelector("form")

    function enableFormEditing() {
        document.querySelectorAll('input').forEach(input => {
            if (input.name !== 'csrfmiddlewaretoken') {
                input.removeAttribute('disabled');
            }
        })

        enableEdit.classList.add("hidden")
        cancelEdit.classList.remove("hidden")
        saveEdit.classList.remove("hidden")
    }

    enableEdit.addEventListener('click', function (e) {
        e.preventDefault()
        enableFormEditing()
    })
})
