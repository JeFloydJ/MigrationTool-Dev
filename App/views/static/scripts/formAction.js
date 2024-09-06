function setAction(action) {
    const form = document.getElementById('upload-form');
    if (action === 'upload') {
        form.action = '/upload';
    } else if (action === 'delete') {
        form.action = '/delete';
    }
}

function toggleInputs() {
    const uploadType = document.getElementById('upload-type').value;
    const folderInput = document.getElementById('folder');
    const filesInput = document.getElementById('files');
    
    if (uploadType === 'folder') {
        folderInput.style.display = 'block';
        filesInput.style.display = 'none';
    } else {
        folderInput.style.display = 'none';
        filesInput.style.display = 'block';
    }
}