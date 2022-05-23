document.addEventListener('DOMContentLoaded', function() {
    let matchMedia = window.matchMedia('(prefers-color-scheme: dark)')
    let systemDarkmode: boolean = matchMedia && matchMedia.matches
    let sessionDarkmode: string = sessionStorage.getItem('preferredColorScheme')
    let darkmodeEnabled: boolean = sessionDarkmode ? sessionDarkmode == 'dark' : systemDarkmode

    const setDarkmodeState = (newState: boolean): void => {
        let darkmodeState: HTMLInputElement = document.getElementById('darkmodeState') as HTMLInputElement
        darkmodeState.checked = !!newState
        setDarkmodeClass(!!newState)
        let preferredColorScheme = !!newState ? 'dark' : 'light'
        sessionStorage.setItem('preferredColorScheme', preferredColorScheme)
    }

    const getDarkmodeState = (): boolean => {
        let darkmodeState: HTMLInputElement = document.getElementById('darkmodeState') as HTMLInputElement
        return darkmodeState.checked
    }

    const setDarkmodeClass = (darkmodeEnabled: boolean | string): void => {
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
