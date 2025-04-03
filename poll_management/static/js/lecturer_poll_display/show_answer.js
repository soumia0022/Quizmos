import { pollState } from '../poll_state.js'

function showAnswer() {
    const closedEyeButton = document.getElementById("show-answer-closed");
    const openEyeButton = document.getElementById("show-answer-open");

    if (typeof window.questions === 'undefined' || typeof window.currentQuestionIndex === 'undefined') {
        return;
    }

    const questionId = window.questions[window.currentQuestionIndex].id;
    if (!questionId) {
        return;
    }

    if (closedEyeButton.style.display === "" || closedEyeButton.style.display === "inline") {
        closedEyeButton.style.display = "none";
        openEyeButton.style.display = "inline";

        pollState.lecturer_webSocket.send(JSON.stringify({
            type: 'show_answers',
            question_id: questionId,
            action: 'show_answer'
        }));
    } else {
        closedEyeButton.style.display = "inline";
        openEyeButton.style.display = "none";

        pollState.lecturer_webSocket.send(JSON.stringify({
            type: 'show_answers',
            question_id: questionId,
            action: 'hide_answer'
        }));
    }
}

window.showAnswer = showAnswer;

module.exports = {showAnswer}