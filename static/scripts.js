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