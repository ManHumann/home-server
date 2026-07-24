console.log("NEW SCRIPT LOADED");

const API_URL = "http://192.168.1.96:8000";

const uploadButton = document.getElementById("uploadButton");

uploadButton.addEventListener("click", uploadImage);

loadImages();


// =========================
// Load Gallery
// =========================

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
                    onclick="openImage('${API_URL}/images/${image.id}')"
                >

                <p>${image.original_filename}</p>

                <div class="button-group">

                    <a
                        href="${API_URL}/images/${image.id}?download=true"
                        class="download-button"
                    >
                        Download
                    </a>

                    <button onclick="deleteImage(${image.id})">
                        Delete
                    </button>

                </div>

            </div>
        `;

    }

}


// =========================
// Upload Image
// =========================

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


// =========================
// Delete Image
// =========================

async function deleteImage(imageId) {

    const confirmed = confirm("Delete this image?");

    if (!confirmed) {
        return;
    }

    const response = await fetch(
        `${API_URL}/images/${imageId}`,
        {
            method: "DELETE"
        }
    );

    if (response.ok) {

        loadImages();

    } else {

        alert("Failed to delete image.");

    }

}


// =========================
// Image Preview
// =========================

function openImage(imageUrl) {

    const modal = document.getElementById("imageModal");

    const modalImage = document.getElementById("modalImage");

    modalImage.src = imageUrl;

    modal.style.display = "flex";

}

function closeImage() {

    document.getElementById("imageModal").style.display = "none";

}
