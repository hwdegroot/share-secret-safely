document.addEventListener("DOMContentLoaded", function () {
    let secretArea = document.getElementById("secret");

    if (secretArea) {
        let accessToken = secretArea.getAttribute("data-access-token")
        let secretId = secretArea.getAttribute("data-secret-id")
        let button = document.getElementById("copy-secret")
        let revealButton = document.getElementById("reveal-secret");
        const classList = Array.from(button.classList)
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
