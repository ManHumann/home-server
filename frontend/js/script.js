const API_URL = "http://192.168.1.96:8000";

async function loadImages() {

    const response = await fetch(`${API_URL}/images/`);

    const images = await response.json();

    const gallery = document.getElementById("gallery");

    gallery.innerHTML = "";

    for (const image of images) {

        gallery.innerHTML += `
            <div class="image-card">

                <img
                    src="${API_URL}/images/${image.id}"
                    alt="${image.original_filename}"
                >

                <p>${image.original_filename}</p>

            </div>
        `;

    }

}

loadImages();

const uploadButton = document.getElementById("uploadButton");

uploadButton.addEventListener("click", uploadImage);

async function uploadImage() {

    const imageInput = document.getElementById("imageInput");

    if (imageInput.files.length === 0) {
        alert("Please select an image.");
        return;
    }

    const formData = new FormData();

    formData.append("file", imageInput.files[0]);

    const response = await fetch(`${API_URL}/images/`, {
        method: "POST",
        body: formData
    });

    if (response.ok) {

        imageInput.value = "";

        loadImages();

    } else {

        alert("Upload failed.");

    }

}
