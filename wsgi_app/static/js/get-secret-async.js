document.addEventListener("DOMContentLoaded", function () {
    let secretArea = document.getElementById("secret");
    if (secretArea) {
        let accessToken = secretArea.getAttribute("data-access-token")
        let secretId = secretArea.getAttribute("data-secret-id")
        let button = document.getElementById("copy-secret")
        const classList = Array.from(button.classList)
        classList.filter(function (cls) {
            return /.*(hover|focus|active):.*/.test(cls)
        }).forEach(function (cls) {
            button.classList.remove(cls)
        })
        axios.get(`/api/secret/${secretId}?jwt=${accessToken}`)
            .then(function (result) {
                secretArea.innerText = result.data.secret
                button.removeAttribute("disabled")
                classList.forEach(function(cls) {
                    button.classList.add(cls)
                })
                button.classList.remove("opacity-50", "cursor-not-allowed")
            })
            .catch(function () {
                secretArea.innerText = "Oops. Unable to retrieve the secret. Please try again 💔"
            })
    }
});
