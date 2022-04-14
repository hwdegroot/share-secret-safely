document.addEventListener("DOMContentLoaded", function () {
    let secretArea = document.getElementById("secret");

    if (secretArea) {
        let accessToken = secretArea.getAttribute("data-access-token")
        let secretId = secretArea.getAttribute("data-secret-id")
        let button = document.getElementById("copy-secret")
        let revealButton = document.getElementById("reveal-secret");
        const classList = Array.from(button.classList)
        if (revealButton) {
            debugger
            secretArea.classList.remove("reveal");
        }
        classList.filter(function (cls) {
            return /.*(hover|focus|active):.*/.test(cls)
        }).forEach(function (cls) {
            button.classList.remove(cls)
        })
        axios.get(`/api/secret/${secretId}?jwt=${accessToken}`)
            .then(function (result) {
                secretArea.innerText = result.data.secret
                button.removeAttribute("disabled")
                revealButton.removeAttribute("disabled")
                classList.forEach(function(cls) {
                    button.classList.add(cls)
                })
                revealButton.classList.remove("opacity-50", "cursor-not-allowed")
                revealButton.addEventListener("click", function() {
                    secretArea.classList.add("reveal");
                    revealButton.remove();
                });
                button.classList.remove("opacity-50", "cursor-not-allowed")
            })
            .catch(function () {
                secretArea.innerText = "Oops. Unable to retrieve the secret. Please try again 💔"
            })
    }
});
