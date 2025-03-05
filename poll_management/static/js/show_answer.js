import { ws } from './websocket.js';

function showAnswer() {
    const closedEyeButton = document.getElementById("show-answer-closed");
    const openEyeButton = document.getElementById("show-answer-open");

    if (closedEyeButton.style.display === "") {
        closedEyeButton.style.display = "none";
        openEyeButton.style.display = "";

        ws.send(JSON.stringify({
            type: 'poll_status',
            action: 'show_answer'
        }));
    } else {
        closedEyeButton.style.display = "";
        openEyeButton.style.display = "none";
    }
}

window.showAnswer = showAnswer;