// https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
document.addEventListener('DOMContentLoaded', () => {
    const copyText: any = (elementId: string) => (): void => {
        let copyText: HTMLInputElement = document.getElementById(elementId) as HTMLInputElement

        if (copyText) {
            window.getSelection().selectAllChildren(copyText)
            // Copy the text inside the text field
            navigator.clipboard.writeText(copyText.value ? copyText.value : copyText.innerText)
            document.getElementById("success-message").classList.remove("hidden")
        }
    }

    let copySecret: HTMLElement = document.getElementById("copy-secret")
    if (copySecret) {
        copySecret.addEventListener("click", copyText("secret"))
    }
    let copyLink: HTMLElement = document.getElementById("copy-link")
    if (copyLink) {
        copyLink.addEventListener("click", copyText("secret-link"))
    }
})
