// https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
document.addEventListener('DOMContentLoaded', function() {
    function copyText(elementId) {
        return function() {
            let copyText = document.getElementById(elementId)

            if (copyText) {
                window.getSelection().selectAllChildren(copyText)
                // Copy the text inside the text field
                navigator.clipboard.writeText(copyText.innerText)
                document.getElementById("success-message").classList.remove("hidden")
            }
        }
    }

    let copySecret = document.getElementById("copy-secret")
    if (copySecret) {
        copySecret.addEventListener("click", copyText("secret"))
    }
    let copyLink = document.getElementById("copy-link")
    if (copyLink) {
        copyLink.addEventListener("click", copyText("secret-link"))
    }
})
