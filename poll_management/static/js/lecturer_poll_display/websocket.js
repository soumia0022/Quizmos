// websocket.js
import {updateMatchResponseUI, updateResponseUI, updateTextResponseUI, updateWordCloudUI, updateCodeResponseUI} from './response_ui.js';
import {displayCorrectAnswer,hideCorrectAnswer} from '../display_correct_answer.js';
import {pollState} from "../poll_state.js";

const wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const wsUrl = `${wsScheme}${window.location.host}/ws/poll/${window.pollCode}/`;
const ws = pollState.lecturer_webSocket = new WebSocket(wsUrl);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === 'new_student') {
        const studentCount = document.getElementById('students-number');
        if (studentCount) {
            studentCount.textContent = data.message;
        }
    }
    if (data.type === 'response_update') {
        // When we receive a response update, fetch the latest counts
        fetchResponseCounts(data.question_id);
    }

    const correctAnswersDiv = document.getElementById('correct-answers');
    if (data.type === 'answers' && data.action === 'show_answer') {
        displayCorrectAnswer(data, correctAnswersDiv);

    } else if (data.action === 'hide_answer') {
        hideCorrectAnswer(correctAnswersDiv);
    }

};

// Function to fetch response counts for a specific question
export async function fetchResponseCounts(questionId) {
    try {
        const response = await fetch(`${window.pollManagementBaseUrl}${window.pollCode}/question/${questionId}/counts/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Received counts:', data);

        if (data.question_type === "text_fill" ){
            updateTextResponseUI(questionId, data.responses);
        }
        else if (data.question_type === "match_question") {
            updateMatchResponseUI(questionId, data);
        }
        else if (data.question_type === "wordcloud"){
            questionId = 'word-cloud-' + questionId
            updateWordCloudUI(questionId, data.word_cloud_data)
        }
        else if (data.question_type === "code_question"){
            updateCodeResponseUI(questionId, data.responses, data.code_language) //has username and code only, need code_language
        }
        else{
            updateResponseUI(questionId, data.counts);
        }
    } catch (error) {
        console.error('Error fetching response counts:', error);
    }
}