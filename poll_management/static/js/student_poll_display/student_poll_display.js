import { startCountdownTimer } from "../timer.js";
import { display_questions } from "./display_questions.js";
import {updateProgressBar} from "./progress_bar.js";
import {displayCorrectAnswer, hideCorrectAnswer} from "../display_correct_answer.js";
import {clean_up_code_mirror} from "../clean_up_code_mirror.js";

const pollState = {
    currentQuestionId: null,
    currentQuestionType: null,
    currentTimerInterval: null,
    currentQuestion: null,
    answerCodeEditor: null,
    totalQuestions: 0,
    currentQuestionNumber: 0,
    webSocket: null
};

function showFeedback(message, isSuccess) {
    const feedback = document.getElementById('feedback');
    feedback.textContent = message;
    feedback.className = `feedback ${isSuccess ? 'success' : 'error'}`;
    feedback.style.display = 'block';
    setTimeout(() => {
        feedback.style.display = 'none';
    }, 3000);
}

// WebSocket message handlers
function handlePollStatus(data) {
    if (data.action === 'lock') {
        showLockOverlay();
    } else if (data.action === 'unlock') {
        hideLockOverlay();
    }
}

function handleAnswers(data) {
    const correctAnswersDiv = document.getElementById('correct-answers');
    if (data.action === 'show_answer') {
        displayCorrectAnswer(data, correctAnswersDiv, pollState);
    } else if (data.action === 'hide_answer') {
        hideCorrectAnswer(correctAnswersDiv, pollState);
    }
}

function handleQuestionDisplay(data) {
    // clear any existing timer
    if (pollState.currentTimerInterval) {
        clearInterval(pollState.currentTimerInterval);
    }

    // reset correct answers display
    const correctAnswersDiv = document.getElementById('correct-answers');
    correctAnswersDiv.style.display = 'none';
    correctAnswersDiv.innerHTML = '';

   clean_up_code_mirror(pollState);

    const questionElement = document.getElementById('question');
    questionElement.innerHTML = data.question.text + '<div class="question-timer"></div>';

    // start timer
    if (data.question.question_timer) {
        pollState.currentTimerInterval = startCountdownTimer(questionElement, data.question.question_timer);
    }

    // update state
    pollState.currentQuestionId = data.question.id;
    pollState.currentQuestionType = data.question.type;
    pollState.currentQuestion = data.question;

    // Display submit button
    document.getElementById('submitResponse').style.display = 'block';

    if (data.total_questions) {
        pollState.totalQuestions = data.total_questions;
    }
    if (data.question_number) {
        pollState.currentQuestionNumber = data.question_number;
    }

    updateProgressBar(pollState.currentQuestionNumber, pollState.totalQuestions);
    display_questions(data);
}

function handleResponseStatus(data) {
    showFeedback(
        data.success ? 'Response submitted successfully!' : "It seems like there's an invalid response, or this question might currently be locked. Please wait for the Lecturer to unlock it.",
        data.success
    );
}

// Response collection based on question type
function collectResponse() {
    switch (pollState.currentQuestionType) {
        case 'multiple_choice':
            return Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                .map(cb => cb.value);

        case 'single_choice':
            const selectedRadio = document.querySelector('input[name="single_choice"]:checked');
            return selectedRadio ? selectedRadio.value : null;

        case 'dropdown_fill':
            const selectedOption = document.querySelector('select').value;
            return selectedOption || null;

        case 'text_fill':
            return document.getElementById('answer').value;

        case 'match_question':
            const matchData = Array.from(document.querySelectorAll('.flex-container')).map(container => {
                const leftOption = container.querySelector('.left').textContent.trim();
                const rightOptionElement = container.querySelector('.dropzone .box');
                const rightOption = rightOptionElement ? rightOptionElement.textContent.trim() : null;
                return {
                    left: leftOption,
                    right: rightOption
                };
            });

            if (matchData.some(match => !match.right)) {
                showFeedback('Please match all items before submitting.', false);
                return null;
            }
            return matchData;

        case 'wordcloud':
            const answer1 = document.getElementById('answer1').value;
            const answer2 = document.getElementById('answer2').value;
            return [answer1, answer2].filter(answer => answer !== '');

        case 'code_question':
            // Get the CodeMirror instance from the text area
            let codeEditor = document.querySelector('.CodeMirror'); // Get the CodeMirror container
            if (codeEditor) {
                let editorInstance = codeEditor.CodeMirror; // Access CodeMirror instance
                return editorInstance.getValue(); // Get the code inside the editor
            } else {
                console.error("CodeMirror instance not found.");
                return "";
            }
    }
    return null;
}

// Event handlers
function handleSubmitResponse() {
    const responseData = collectResponse();

    if (responseData && responseData.length !== 0) {
        pollState.webSocket.send(JSON.stringify({
            type: 'response',
            question_id: pollState.currentQuestionId,
            response_type: pollState.currentQuestionType,
            response_data: responseData
        }));
    } else {
        showFeedback('Please provide a response', false);
    }
}

function handleWebSocketMessage(event) {
    const data = JSON.parse(event.data);

    switch (data.type) {
        case 'poll_status':
            handlePollStatus(data);
            break;
        case 'answers':
            handleAnswers(data);
            break;
        case 'question':
            handleQuestionDisplay(data);
            break;
        case 'response_status':
            handleResponseStatus(data);
            break;
    }
}

// Initialization
function initializeWebSocket(pollCode) {
    const ws = new WebSocket(`ws://${window.location.host}/ws/poll/${pollCode}/`);
    ws.onmessage = handleWebSocketMessage;
    return ws;
}

function initializeEventListeners() {
    document.getElementById('submitResponse').addEventListener('click', handleSubmitResponse);
}

// Main initialization function
function initialize() {
    const pollCodeElement = document.getElementById('poll-container');
    const pollCode = pollCodeElement ? pollCodeElement.dataset.pollCode : null;

    if (!pollCode) {
        console.error("Poll code not found");
        return;
    }

    pollState.webSocket = initializeWebSocket(pollCode);
    initializeEventListeners();
    createLockOverlay();
}

// Start the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', initialize);