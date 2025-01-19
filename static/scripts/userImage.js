function previewImage(event) {
    const file = event.target.files[0];
    const chooseText = document.getElementById('chooseText');
    const img = document.getElementById('imagePreview');
    if (!file) {
        console.log("No file selected");
        return;
    }
    const reader = new FileReader();

    reader.onload = function(e) {
        console.log("File loaded", e.target.result);
        img.src = e.target.result;
        img.style.display = 'block';
        chooseText.style.display = 'none';
    };
    reader.onerror = function(e) {
        console.log("Error loading file", e);
    };
    if (file) {
        reader.readAsDataURL(file);
    }
}
function clearImage() {
    const fileInput = document.getElementById('user_image');
    fileInput.value = '';
    const img = document.getElementById('imagePreview');
    img.style.display = 'none';
    img.src = '';
    const chooseText = document.getElementById('chooseText');
    chooseText.style.display = 'block';
}
