document.addEventListener('DOMContentLoaded', function() {
    let matchMedia = window.matchMedia('(prefers-color-scheme: dark)')
    let systemDarkmode = matchMedia && matchMedia.matches
    let sessionDarkmode = sessionStorage.getItem('preferredColorScheme')
    let darkmodeEnabled = sessionDarkmode ? sessionDarkmode == 'dark' : systemDarkmode

    function setDarkmodeState(newState) {
        let darkmodeState = document.getElementById('darkmodeState')
        darkmodeState.checked = !!newState
        setDarkmodeClass(!!newState)
        let preferredColorScheme = !!newState ? 'dark' : 'light'
        sessionStorage.setItem('preferredColorScheme', preferredColorScheme)
    }

    function getDarkmodeState() {
        let darkmodeState = document.getElementById('darkmodeState')
        return darkmodeState.checked
    }

    function setDarkmodeClass(darkmodeEnabled) {
        if (darkmodeEnabled) {
            document.body.classList.add('dark')
        } else {
            document.body.classList.remove('dark')
        }
    }

    setDarkmodeState(darkmodeEnabled)

    document.getElementById('setDarkmode').addEventListener('click', function () { setDarkmodeState(true) })
    document.getElementById('setLightmode').addEventListener('click', function () { setDarkmodeState(false) })

    document.getElementById('darkmodeToggle')
        .addEventListener('click', function (e) {
            setDarkmodeState(!getDarkmodeState())
        })
});
