document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('keydown', event => {
        if(event.key === 'F5' || event.key === 'Escape') {
            event.preventDefault();

            sessionStorage.removeItem('pageWasVisited')
            window.location.href = '../index.html';
        }
    })
})

document.addEventListener('DOMContentLoaded', () => {
    const fileUpload = document.getElementById('file__upload');
    const imagesButton = document.getElementById('images-tab-btn');
    const dropzone = document.querySelector('.upload__dropzone');
    const currentUploadInput = document.querySelector('.upload__input');
    const copyButton = document.querySelector('.upload__copy');

    const updateTabStyles = () => {
        const uploadTab = document.getElementById('upload-tab-btn');
        const imagesTab = document.getElementById('images-tab-btn');
        const storedFiles = JSON.parse(localStorage.getItem('uploadedImages')) || [];

        const isImagesPage = window.location.pathname.includes('images.html');

        uploadTab.classList.remove('upload__tab--active');
        imagesTab.classList.remove('upload__tab--active');

        if(isImagesPage) {
            imagesTab.classList.add('upload__tab--active')
        } else {
            uploadTab.classList.remove('upload__tab--active');
        }
    };

    const handleAndStoresFile = (files) => {
        if (!files || files.length === 0) return;

        const storedFiles = JSON.parse(localStorage.getItem('uploadedImages')) || [];
        const allowedTypes = ['image/png', 'image/gif', 'image/jpeg'];
        const MAX_FILE_SIZE = 5;
        const MAX_SIZE_BYTES = MAX_FILE_SIZE * 1024 * 1024;
        let filesAdded = false;
        let lastFileName = '';

        for(const file of files){
            if(!allowedTypes.includes(file.type) || file.size > MAX_SIZE_BYTES){
                continue;
            }
            const reader = new FileReader();
            reader.onload = event => {
                const fileData = {name: file.name, url: event.target.result};
                storedFiles.push(fileData);
                localStorage.setItem('uploadedImages', JSON.stringify(storedFiles));
                updateTabStyles();
            };
            reader.readAsDataURL(file);
            filesAdded = true;
            lastFileName = file.name;
        }
        if (filesAdded) {
            if (currentUploadInput) {
                currentUploadInput.value = `https://sharefile.xyz${lastFileName}`;
            }
            alert("Files selected successfully! Go to the 'Images' tab to view them.");
        }
    };

    if (copyButton && currentUploadInput) {
        copyButton.addEventListener('click', event => {
            const textToCopy = currentUploadInput.value;

            if (textToCopy && textToCopy !== 'https://') {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    copyButton.textContent = 'COPIED!';
                    setTimeout(() => {
                        copyButton.textContent = 'COPY';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy', err);
                });
            }
        });
    }

    if (imagesButton) {
        imagesButton.addEventListener('click', event => {
            window.location.href = '../form/images.html'
        });
    }

    fileUpload.addEventListener('change', event => {
        handleAndStoresFile(event.target.files);
        event.target.value = '';
    });

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    dropzone.addEventListener('drop', event => {
        handleAndStoresFile(event.dataTransfer.files);
    });

    updateTabStyles();
});