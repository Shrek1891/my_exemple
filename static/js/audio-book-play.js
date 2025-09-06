const playButton = document.getElementById('playButton')
const audio = document.getElementById('audioPlayer')
const loaderWrapper = document.getElementById('loader-wrapper');

playButton.addEventListener('click', () => {
    if (audio.paused) {
        audio.play()
        playButton.textContent = 'Pause'
    } else {
        audio.pause()
        playButton.textContent = 'Play'
    }
})

const load_audio = async () => {
    loaderWrapper.hidden = false
    const response = await fetch('/projects/audio-book/get_audio')
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    audio.src = url
    loaderWrapper.hidden = true
    return url
}

const play_audio = () => {
    audio.load()
    audio.play()
    playButton.textContent = 'Pause'
}
load_audio()
play_audio()

audio.addEventListener('ended', async () => {
    await load_audio()
    play_audio()
})