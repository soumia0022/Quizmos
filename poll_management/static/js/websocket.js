// websocket.js
import {updateMatchResponseUI, updateResponseUI, updateTextResponseUI} from './response_ui.js';

const wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const wsUrl = `${wsScheme}${window.location.host}/ws/poll/${pollCode}/`;
export const ws = new WebSocket(wsUrl);

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

    if (data.type === 'question') {
        if (data.question) {  
            const currentQuestionNumber = data.question.question_number;
            const totalQuestions = data.question.total_questions;
        } 
    }
};

// Function to update the progress bar
function updateProgressBar(currentNum, total) {
    const progressBar = document.getElementById('question-progress-bar');
    const progressText = document.getElementById('question-progress-text');

    if (!progressBar || !progressText) return;

    const percentage = total > 0 ? (currentNum / total) * 100 : 0;
    progressBar.style.width = `${percentage}%`;
    progressBar.setAttribute('aria-valuenow', percentage);
    progressText.textContent = `Question ${currentNum} of ${total}`;
}

// Function to fetch response counts for a specific question
async function fetchResponseCounts(questionId) {
    try {
        const response = await fetch(`${window.pollManagementBaseUrl}${pollCode}/question/${questionId}/counts/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Received counts:', data);

        if (data.question_type === "text_fill" || data.question_type === "wordcloud"){//update this later when word cloud responses is done
            updateTextResponseUI(questionId, data.responses);
        }
        else if (data.question_type === "match_question") {
            updateMatchResponseUI(questionId, data);
        }
        else{
            updateResponseUI(questionId, data.counts);
        }


    } catch (error) {
        console.error('Error fetching response counts:', error);
    }
}