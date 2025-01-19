const faviconTag = document.getElementById("faviconTag");
const isDark = window.matchMedia("(prefers-color-scheme: dark)");
const changeFavicon = () => {
    if (isDark.matches) {
        faviconTag.href = "../../static/assets/root/images/core/logo.svg";
    } else {
        faviconTag.href = "../../static/assets/root/images/core/logo-dark.svg";
    }
};
changeFavicon();
isDark.addEventListener("change", changeFavicon);
