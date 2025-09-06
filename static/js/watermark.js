const loaderWrapper = document.getElementById('loader-wrapper');
const uploadButton = document.getElementById('uploadButton');
const form = document.querySelector('form');

uploadButton.addEventListener('click', (e) => {
    if (form.checkValidity()) {
        loaderWrapper.hidden = false;
    }

})