document.addEventListener('DOMContentLoaded', function() {
    const wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const wsUrl = `${wsScheme}${window.location.host}/ws/poll/${pollCode}/`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = function() {
        console.log("WebSocket connected!");
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.type === 'new_student') {
            const studentCount = document.getElementById('students-number');
            studentCount.textContent= data.message;
        }
    };

});