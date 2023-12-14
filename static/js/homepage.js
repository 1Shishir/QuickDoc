

const dropArea = document.getElementById('dropArea');
const fileButton = document.getElementById('fileButton');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropArea.classList.add('drag');
}

function unhighlight(e) {
    dropArea.classList.remove('drag');
}

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files || dt.items;

    handleFiles(files);
}

fileButton.addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

const fileInput = document.createElement('input');
fileInput.setAttribute('type', 'file');
fileInput.setAttribute('id', 'fileInput');
fileInput.setAttribute('multiple', '');
fileInput.style.display = 'none';

fileInput.addEventListener('change', handleFileSelect, false);
document.body.appendChild(fileInput);

function handleFileSelect(e) {
    let files = e.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        console.log(file);
        console.log(file.size);


    }
}
















