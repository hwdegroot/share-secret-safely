import axios from "axios"

document.addEventListener("DOMContentLoaded", function () {
    const secretArea: HTMLElement = document.getElementById("secret");

    if (secretArea) {
        const accessToken: string = secretArea.getAttribute("data-access-token")
        const secretId: string = secretArea.getAttribute("data-secret-id")
        const button: HTMLInputElement = document.getElementById("copy-secret") as HTMLInputElement
        const revealButton: HTMLInputElement = document.getElementById("reveal-secret") as HTMLInputElement
        const classList: Array<string> = Array.from(button.classList)
        if (revealButton) {
            secretArea.classList.remove("reveal");
        }
        classList.filter(function (cls) {
            return /.*(hover|focus|active):.*/.test(cls)
        }).forEach(function (cls) {
            button.classList.remove(cls)
        })
        axios.get(`/api/secret/${secretId}?jwt=${accessToken}`)
            .then(function (result) {
                secretArea.innerHTML = result.data.secret
                button.removeAttribute("disabled")
                classList.forEach(function(cls) {
                    button.classList.add(cls)
                })
                if (revealButton) {
                    revealButton.removeAttribute("disabled")
                    revealButton.classList.remove("opacity-50", "cursor-not-allowed")
                    revealButton.addEventListener("click", function() {
                        if (secretArea.classList.contains("reveal")) {
                            secretArea.classList.remove("reveal");
                            revealButton.innerText = "reveal";
                            revealButton.classList.remove("hide-secret")
                        } else {
                            secretArea.classList.add("reveal");
                            revealButton.innerText = "unreveal";
                            revealButton.classList.remove("show-secret")
                        }
                    });
                }
                button.classList.remove("opacity-50", "cursor-not-allowed")
            })
            .catch(function () {
                secretArea.innerText = "Oops. Unable to retrieve the secret. Please try again 💔"
            })
    }
});
