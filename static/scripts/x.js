const closeBtn = document.getElementById('closeBtn');
const testimonialsPanel = document.getElementById('testimonialsPanel');
closeBtn.addEventListener('click', function() {
    testimonialsPanel.classList.add('hidden');
});