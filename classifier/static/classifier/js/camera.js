// Camera handling for capturing tobacco leaf images

let video = null;
let canvas = null;
let streaming = false;
let cameraWidth = 320;
let cameraHeight = 0;

function initCamera() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-button');
    const errorMessage = document.getElementById('camera-error');
    
    // If elements don't exist, don't proceed
    if (!video || !canvas || !captureButton) return;
    
    // Hide error message initially
    if (errorMessage) errorMessage.classList.add('d-none');
    
    // Check if we already have a stream running
    if (streaming) return;
    
    // Get user media with constraints
    navigator.mediaDevices.getUserMedia({
        video: {
            facingMode: 'environment', // Prefer rear camera on mobile
            width: { ideal: 1280 },
            height: { ideal: 720 }
        },
        audio: false
    })
    .then(function(stream) {
        // Set video source to the stream
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.error("Error accessing camera:", err);
        if (errorMessage) {
            errorMessage.classList.remove('d-none');
            errorMessage.textContent = "Error accessing camera: " + err.message;
        }
    });
    
    // When video starts playing
    video.addEventListener('canplay', function() {
        if (!streaming) {
            // Calculate height based on width to maintain aspect ratio
            cameraHeight = video.videoHeight / (video.videoWidth / cameraWidth);
            
            // Handle NaN result
            if (isNaN(cameraHeight)) {
                cameraHeight = cameraWidth / (4/3);
            }
            
            // Set video dimensions
            video.setAttribute('width', cameraWidth);
            video.setAttribute('height', cameraHeight);
            
            // Set canvas dimensions
            canvas.setAttribute('width', video.videoWidth);
            canvas.setAttribute('height', video.videoHeight);
            
            streaming = true;
        }
    }, false);
    
    // Capture button click handler
    captureButton.addEventListener('click', function() {
        if (streaming) {
            takePicture();
        }
    });
}

function takePicture() {
    const context = canvas.getContext('2d');
    
    // If we have valid dimensions
    if (canvas.width && canvas.height) {
        // Draw video frame to canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Get image data as base64
        const imageData = canvas.toDataURL('image/jpeg');
        
        // Show image preview
        const preview = document.getElementById('capture-preview');
        if (preview) {
            preview.src = imageData;
            preview.classList.remove('d-none');
        }
        
        // Store in hidden form field
        const imageDataInput = document.getElementById('imageData');
        if (imageDataInput) {
            imageDataInput.value = imageData;
        }
        
        // Show submit button
        const submitButton = document.getElementById('submit-capture-button');
        if (submitButton) {
            submitButton.classList.remove('d-none');
        }
        
        // Show retake button
        const retakeButton = document.getElementById('retake-button');
        if (retakeButton) {
            retakeButton.classList.remove('d-none');
        }
        
        // Hide capture button
        const captureButton = document.getElementById('capture-button');
        if (captureButton) {
            captureButton.classList.add('d-none');
        }
        
        // Hide video
        if (video) {
            video.classList.add('d-none');
        }
    }
}

function retakePicture() {
    // Hide preview
    const preview = document.getElementById('capture-preview');
    if (preview) {
        preview.classList.add('d-none');
    }
    
    // Clear hidden form field
    const imageDataInput = document.getElementById('imageData');
    if (imageDataInput) {
        imageDataInput.value = '';
    }
    
    // Hide submit button
    const submitButton = document.getElementById('submit-capture-button');
    if (submitButton) {
        submitButton.classList.add('d-none');
    }
    
    // Hide retake button
    const retakeButton = document.getElementById('retake-button');
    if (retakeButton) {
        retakeButton.classList.add('d-none');
    }
    
    // Show capture button
    const captureButton = document.getElementById('capture-button');
    if (captureButton) {
        captureButton.classList.remove('d-none');
    }
    
    // Show video
    if (video) {
        video.classList.remove('d-none');
    }
}

function submitCapturedImage() {
    // Check if we have an image
    const imageDataInput = document.getElementById('imageData');
    if (!imageDataInput || !imageDataInput.value) {
        showAlert('No image captured. Please take a picture first.', 'danger');
        return false;
    }
    
    // Show loading state
    const submitButton = document.getElementById('submit-capture-button');
    if (submitButton) {
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
        submitButton.disabled = true;
    }
    
    // Get form
    const form = document.getElementById('camera-form');
    
    // Submit form via AJAX
    if (form) {
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                showAlert('Error processing the image. Please try again.', 'danger');
                if (submitButton) {
                    submitButton.innerHTML = 'Submit';
                    submitButton.disabled = false;
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error processing the image. Please try again.', 'danger');
            if (submitButton) {
                submitButton.innerHTML = 'Submit';
                submitButton.disabled = false;
            }
        });
    }
    
    return false;
}

// Stop the camera stream when leaving the page
window.addEventListener('beforeunload', function() {
    if (video && video.srcObject) {
        const tracks = video.srcObject.getTracks();
        tracks.forEach(track => track.stop());
    }
});
