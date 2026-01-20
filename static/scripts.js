function changeLanguage(lang) {
  window.location.href = "/?lang=" + lang;
}

async function showEmail() {
  const response = await fetch('/get-contact-email');
  const data = await response.json();
  document.getElementById('contact-email').innerText = data.email;
  document.getElementById('show-email-btn').hidden = true;
}

document.addEventListener('DOMContentLoaded', function() {
    const languageMenu = document.getElementById('language-menu');
    if (languageMenu) {
        languageMenu.addEventListener('click', function(event) {
            const target = event.target.closest('a[data-lang]');
            if (target) {
                event.preventDefault();
                const language = target.getAttribute('data-lang');

                // Track language selection with Google Analytics
                if (typeof gtag === 'function') {
                    gtag('event', 'language_select', {
                        'event_category': 'engagement',
                        'event_label': language
                    });
                }

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

    const searchInput = document.getElementById('language-search');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase();
            const languageMenu = document.getElementById('language-menu');
            const items = languageMenu.getElementsByTagName('li');
            const divider = document.getElementById('language-divider');

            if (filter) {
                if(divider) divider.parentElement.style.display = "none";
            } else {
                if(divider) divider.parentElement.style.display = "";
            }

            for (let i = 0; i < items.length; i++) {
                // Don't filter the search input itself
                if (items[i].contains(searchInput)) {
                    continue;
                }

                const a = items[i].getElementsByTagName('a')[0];
                if (a) {
                    const txtValue = a.textContent || a.innerText;
                    if (txtValue.toLowerCase().indexOf(filter) > -1) {
                        items[i].style.display = "";
                    } else {
                        items[i].style.display = "none";
                    }
                }
            }
        });

        // Prevent dropdown from closing when clicking on the search input
        searchInput.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    }
});