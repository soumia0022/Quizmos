export class WebSocketManager {
    constructor(pollCode) {
        this.pollCode = pollCode;
        this.wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        this.wsUrl = `${this.wsScheme}${window.location.host}/ws/poll/${pollCode}/`;
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.wsUrl);
        this.ws.onopen = () => console.log("WebSocket connected");
        this.ws.onerror = (error) => console.error("WebSocket error:", error);
        this.ws.onclose = () => console.log("WebSocket closed");
        this.ws.onmessage = (event) => this.handleMessage(event);
    }

    handleMessage(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'message') {
            this.updateStudentsList(data.message);
            this.updateStudentCounter()
        }
    }

    updateStudentsList(message) {
        const studentsList = document.getElementById('students-list');
        const newStudent = document.createElement('li');

        newStudent.textContent = message;
        studentsList.appendChild(newStudent);
    }

    updateStudentCounter() {
    const counter = document.getElementById('student-count');
    let currentCount = parseInt(counter.textContent, 10);
    currentCount += 1;
    counter.textContent = currentCount;
    }

}