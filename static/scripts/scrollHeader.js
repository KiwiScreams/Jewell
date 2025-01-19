let lastScrollToTop = 0;
let navbar = document.getElementById("navbar");
console.log("scrollHeader");
window.addEventListener("scroll", function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollTop > lastScrollToTop) {
        navbar.style.top = "-150px";
    }
    else {
        navbar.style.top = "0px";
    }
    lastScrollToTop = scrollTop;
});
