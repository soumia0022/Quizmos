const magnifyIcon = document.getElementById('magnify');
const qrOverlay = document.getElementById('qrOverlay');
const closeButton = document.getElementById('close');

magnifyIcon.addEventListener('click', function() {
qrOverlay.style.display = 'block';
});

closeButton.addEventListener('click', function() {
qrOverlay.style.display = 'none';
});