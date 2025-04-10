function initializeDragAndDrop() {
    const rightContainer = document.getElementById('right');

    if (rightContainer) {
        new Sortable(rightContainer, {
            group: 'shared',
            animation: 150,
            sort: false, 
        });
    }

    const dropzones = document.querySelectorAll('.dropzone');
    dropzones.forEach((dropzone) => {
        new Sortable(dropzone, {
            group: 'shared',
            animation: 150,
            onAdd: function (evt) {
                if (dropzone.children.length > 1) {
                    const oldItem = dropzone.children[0];
                    rightContainer.appendChild(oldItem);
                }
                evt.item.classList.add("matched-item"); 
            },
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    initializeDragAndDrop();
});
