const searchBtn = document.getElementById("searchBtn");
const searchSection = document.getElementById("searchSection");
const closeSearchBtn = document.getElementById("closeSearch");
searchBtn.addEventListener("click", function() {
    if (searchSection.style.display === "none" || searchSection.style.display === "") {
        searchSection.style.display = "block";
        setTimeout(function() {
            searchSection.classList.add("show");
            searchSection.classList.remove("end");
        }, 10);
    } else {
        searchSection.classList.add("end");
        setTimeout(function() {
            searchSection.style.display = "none";
        }, 300);
    }
});
closeSearchBtn.addEventListener("click", function() {
    searchSection.classList.add("end");
    setTimeout(function() {
        searchSection.style.display = "none";
    }, 300);
});
