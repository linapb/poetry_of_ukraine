//function changeLanguage(lang) {
//    var xhr = new XMLHttpRequest();
//    xhr.open("GET", "/?lang=" + lang, true);
//    alert("Language changed to: " + lang);
//    xhr.send();
//
//}

function changeLanguage(lang) {
    window.location.href = "/?lang=" + lang;
}

document.addEventListener('DOMContentLoaded', function() {
    const languageMenu = document.getElementById('language-menu');
    if (languageMenu) {
        languageMenu.addEventListener('click', function(event) {
            const target = event.target.closest('a[data-lang]');
            if (target) {
                event.preventDefault();
                const language = target.getAttribute('data-lang');

                // Show spinner
                const spinnerOverlay = document.getElementById('spinner-overlay');
                if (spinnerOverlay) {
                    spinnerOverlay.style.display = 'flex';
                }

                changeLanguage(language);
            }
        });
    }

    const rays = document.querySelectorAll('.sun-ray');
    const rayCount = rays.length;
    rays.forEach((ray, i) => {
        const angle = (360 / rayCount) * i;
        ray.style.transform = `rotate(${angle}deg) translateY(-40px)`;
    });
});