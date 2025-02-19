// websocket.js
import {updateResponseUI, updateTextResponseUI} from './response_ui.js';

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
};

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
        else{
            updateResponseUI(questionId, data.counts);
        }


    } catch (error) {
        console.error('Error fetching response counts:', error);
    }
}