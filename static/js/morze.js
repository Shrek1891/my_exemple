const form = document.querySelector('form');
const loaderWrapper = document.getElementById('loader-wrapper');

window.addEventListener('click', (e) => {
    if (e.target.id === 'translateButton') {
        if (form.checkValidity()) {
            loaderWrapper.hidden = false;
        }
    }
    if (e.target.id === 'copyButton') {
        const textToCopy = document.getElementById('textToCopy');
        const copyButton = document.getElementById('copyButton');
        const text = textToCopy.textContent.trim();
        navigator.clipboard.writeText(text).then(() => {
            copyButton.textContent = 'Copied!';
            copyButton.disabled = true;
            copyButton.classList.add('btn-success');
        });
    }
})


