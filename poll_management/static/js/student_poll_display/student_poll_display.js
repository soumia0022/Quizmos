import { startCountdownTimer } from "../timer.js";
import { display_questions } from "./display_questions.js";
import { updateProgressBar } from "./progress_bar.js";
import { displayCorrectAnswer, hideCorrectAnswer } from "../display_correct_answer.js";
import { clean_up_code_mirror } from "../clean_up_code_mirror.js";
import { showFeedback } from "./show_feedback.js";
import { collectResponse } from "./collect_responses.js";
import { pollState } from "../poll_state.js";
import { createLockOverlay } from "./student_lock.js";

// WebSocket message handlers
function handlePollStatus(data) {
    if (data.action === 'lock') {
        showLockOverlay();
    } else if (data.action === 'unlock') {
        hideLockOverlay();
    }
}

function handleLecturerStatus(data) {
    const submitButton = document.getElementById("submitResponse");

    if (data.action === 'disconnected') {
        // Lecturer has disconnected
        pollState.lecturerConnected = false;
        submitButton.disabled = true;

        // Show disconnect message
        showLecturerDisconnectedMessage();
    } else if (data.action === 'connected') {
        // Lecturer has connected
        pollState.lecturerConnected = true;
        submitButton.disabled = false;

        // Hide disconnect message
        hideLecturerDisconnectedMessage();
    }
}

function handleAnswers(data) {
    const correctAnswersDiv = document.getElementById('correct-answers');
    if (data.action === 'show_answer') {
        displayCorrectAnswer(data, correctAnswersDiv);
    } else if (data.action === 'hide_answer') {
        hideCorrectAnswer(correctAnswersDiv);
    }
}

function handleQuestionDisplay(data) {
    // clear any existing timer
    const submitButton = document.getElementById("submitResponse");

    if (submitButton.disabled === true && pollState.lecturerConnected) {
        submitButton.disabled = false;
    }

    if (pollState.currentTimerInterval) {
        clearInterval(pollState.currentTimerInterval);
    }

    // reset correct answers display
    const correctAnswersDiv = document.getElementById('correct-answers');
    correctAnswersDiv.style.display = 'none';
    correctAnswersDiv.innerHTML = '';

    clean_up_code_mirror();

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
    // Only show successful submission if lecturer is connected
    if (data.success && !pollState.lecturerConnected) {
        showFeedback('The lecturer has disconnected. Your response cannot be received at this time.', false);
    } else {
        showFeedback(
            data.success ? 'Response submitted successfully!' : "It seems like there's an invalid response, or this question might currently be locked. Please wait for the Lecturer to unlock it.",
            data.success
        );
    }
}

// Event handlers
function handleSubmitResponse() {
    // Prevent submission if lecturer is disconnected
    if (!pollState.lecturerConnected) {
        showFeedback('The lecturer has disconnected. Your response cannot be submitted at this time.', false);
        return;
    }

    const responseData = collectResponse();
    if (responseData && responseData.length !== 0) {
        pollState.student_webSocket.send(JSON.stringify({
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
        case 'lecturer_status':
            handleLecturerStatus(data);
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

function showLecturerDisconnectedMessage() {
    // Remove any existing notices
    hideLecturerDisconnectedMessage();

    // Create a warning banner
    const disconnectBanner = document.createElement('div');
    disconnectBanner.id = 'lecturer-disconnected-banner';
    disconnectBanner.style.backgroundColor = '#f8d7da';
    disconnectBanner.style.color = '#721c24';
    disconnectBanner.style.padding = '10px';
    disconnectBanner.style.margin = '10px 0';
    disconnectBanner.style.borderRadius = '5px';
    disconnectBanner.style.textAlign = 'center';
    disconnectBanner.innerHTML = 'The lecturer has disconnected. Responses cannot be submitted at this time.';

    const pollContainer = document.getElementById('poll-container');
    pollContainer.insertBefore(disconnectBanner, pollContainer.firstChild);
}

function hideLecturerDisconnectedMessage() {
    const existingBanner = document.getElementById('lecturer-disconnected-banner');
    if (existingBanner) {
        existingBanner.remove();
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

    pollState.student_webSocket = initializeWebSocket(pollCode);
    initializeEventListeners();
    createLockOverlay();
}

// Start the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', initialize);