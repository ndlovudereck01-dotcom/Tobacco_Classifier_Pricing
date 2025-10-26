// Main JavaScript for the tobacco classification app

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the file upload functionality
    initFileUpload();
    
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Show processing spinner when form is submitted
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Disable button and show spinner
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            }
            
            // Show processing overlay
            const processingOverlay = document.getElementById('processing-overlay');
            if (processingOverlay) {
                processingOverlay.classList.remove('d-none');
            }
        });
    });
});

function initFileUpload() {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('imageUpload');
    
    if (!uploadArea || !fileInput) return;
    
    // File upload area event listeners
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('highlight');
    });
    
    uploadArea.addEventListener('dragleave', function() {
        uploadArea.classList.remove('highlight');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('highlight');
        
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelected(fileInput);
        }
    });
    
    // File input change event
    fileInput.addEventListener('change', function() {
        handleFileSelected(this);
    });
}

function handleFileSelected(fileInput) {
    if (fileInput.files && fileInput.files[0]) {
        const file = fileInput.files[0];
        
        // Show image preview
        const preview = document.getElementById('image-preview');
        if (preview) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.parentElement.classList.remove('d-none');
            };
            reader.readAsDataURL(file);
        }
        
        // Update file name display
        const fileNameDisplay = document.getElementById('file-name');
        if (fileNameDisplay) {
            fileNameDisplay.textContent = file.name;
        }
        
        // Show submit button
        const submitButton = document.getElementById('submit-button');
        if (submitButton) {
            submitButton.classList.remove('d-none');
        }
    }
}

// Function to validate image before submitting
function validateImageUpload() {
    const fileInput = document.getElementById('imageUpload');
    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        showAlert('Please select an image to upload.', 'danger');
        return false;
    }
    
    const file = fileInput.files[0];
    const fileType = file.type;
    const validImageTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    
    if (!validImageTypes.includes(fileType)) {
        showAlert('Please select a valid image file (JPEG, PNG).', 'danger');
        return false;
    }
    
    if (file.size > 5 * 1024 * 1024) { // 5MB
        showAlert('Image size should be less than 5MB.', 'danger');
        return false;
    }
    
    return true;
}

// Function to display alerts
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) return;
    
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show`;
    alertElement.role = 'alert';
    
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alertElement);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertElement.classList.remove('show');
        setTimeout(() => {
            alertsContainer.removeChild(alertElement);
        }, 150);
    }, 5000);
}

// Function to toggle between file upload and camera
function toggleUploadMethod(method) {
    const fileUploadContainer = document.getElementById('file-upload-container');
    const cameraContainer = document.getElementById('camera-container');
    const fileTab = document.getElementById('file-tab');
    const cameraTab = document.getElementById('camera-tab');
    
    if (method === 'file') {
        fileUploadContainer.classList.remove('d-none');
        cameraContainer.classList.add('d-none');
        fileTab.classList.add('active');
        cameraTab.classList.remove('active');
    } else if (method === 'camera') {
        fileUploadContainer.classList.add('d-none');
        cameraContainer.classList.remove('d-none');
        fileTab.classList.remove('active');
        cameraTab.classList.add('active');
        
        // Initialize camera
        initCamera();
    }
}
