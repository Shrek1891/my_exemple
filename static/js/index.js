document.addEventListener(
    "DOMContentLoaded",
    function () {
        const allLinks = document.querySelectorAll("a.nav-link");
        const currentPath = window.location.pathname.split("/").reverse()[0];
        for (let i = 0; i < allLinks.length; i++) {
            allLinks[i].classList.remove("active");
        }
        for (let i = 0; i < allLinks.length; i++) {

            if (allLinks[i].href.split("/").reverse()[0] === currentPath) {
                allLinks[i].classList.add("active");
            }
        }

    }
)





