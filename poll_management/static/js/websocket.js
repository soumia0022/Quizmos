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
            const studentsList = document.getElementById('students-list');
            const newStudent = document.createElement('li');
            newStudent.textContent = data.message;
            newStudent.className = 'list-group-item';

            studentsList.appendChild(newStudent);
        }
    };

});