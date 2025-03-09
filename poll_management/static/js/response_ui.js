import {WordCloudGenerator} from "./word_could_generator.js";

function updateProgressElements(element, count, totalResponses) {
    const percentage = totalResponses > 0 ? (count / totalResponses) * 100 : 0;
    const percentageElement = element.querySelector('.response-percentage');
    const countElement = element.querySelector('.response-count');
    const progressBar = element.querySelector('.progress-bar');

    if (percentageElement && countElement && progressBar) {
        percentageElement.textContent = `${percentage.toFixed(1)}%`;
        countElement.textContent = `(${count})`;
        progressBar.style.width = `${percentage}%`;


        if (count > 0) {
            element.classList.add('has-responses');
            progressBar.classList.add('bg-primary');
        } else {
            element.classList.remove('has-responses');
            progressBar.classList.remove('bg-primary');
        }
    }

    return percentage;
}

export function updateResponseUI(questionId, optionCounts, questionType) {
    //for single, multiple choice and drop down questions
    const questionContainer = document.querySelector(`[data-question="${questionId}"]`);
    const cards = questionContainer.querySelectorAll('.response-card');

    const totalResponses = Object.values(optionCounts).reduce((a, b) => a + b, 0);


    cards.forEach((card, index) => {
        const count = optionCounts[index] || 0;
        updateProgressElements(card, count, totalResponses);
    });
}

export function updateTextResponseUI(questionId, responses) {
    //for text answered questions
    const questionContainer = document.querySelector(`[data-question="${questionId}"]`);
    const responseList = questionContainer.querySelector(`#responseList-${questionId}`);


    responseList.innerHTML = '';

    // add the responses as a list on the screen maybe update later to be able to delete
    responses.forEach((response) => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span class="response-text">${response}</span>
            </div>
        `;
        responseList.appendChild(listItem);
    });


    const responseListContainer = questionContainer.querySelector('.response-list-container');
    if (responseListContainer) {
        responseListContainer.style.display = responses.length > 0 ? 'block' : 'none';
    }
}

export function updateCodeResponseUI(questionId, responses) {
    const questionContainer = document.querySelector(`[data-question="${questionId}"]`);
    const responseList = questionContainer.querySelector(`#responseList-${questionId}`);

    responseList.innerHTML = '';

    responses.forEach((response) => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';

        // Display user’s name and make it clickable to show code in the editor
        listItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span class="response-user" style="cursor: pointer; color: blue;" data-code="${encodeURIComponent(response.code)}">
                    ${response.username}
                </span>
            </div>
        `;

        responseList.appendChild(listItem);

        // Add event listener to show code in CodeMirror when user clicks on their name
        listItem.querySelector('.response-user').addEventListener('click', function () {
            const code = decodeURIComponent(this.getAttribute('data-code'));
            displayCodeInEditor(code);
        });
    });

    // Show or hide response list container
    const responseListContainer = questionContainer.querySelector('.response-list-container');
    if (responseListContainer) {
        responseListContainer.style.display = responses.length > 0 ? 'block' : 'none';
    }
}

// Function to display code inside a CodeMirror editor
function displayCodeInEditor(code) {
    // Ensure there's a textarea available for CodeMirror
    let codeEditorTextarea = document.getElementById('code-editor');
    if (!codeEditorTextarea) {
        console.error('Code editor textarea not found!');
        return;
    }

    // If CodeMirror is already initialized, update its content
    if (window.codeEditorInstance) {
        window.codeEditorInstance.setValue(code);
    } else {
        // Initialize CodeMirror and store reference globally
        window.codeEditorInstance = CodeMirror.fromTextArea(codeEditorTextarea, {
            mode: "python", // Adjust language dynamically later
            theme: "default",
            lineNumbers: true,
            readOnly: true // Set to read-only to prevent editing
        });

        // Set the code after initializing
        window.codeEditorInstance.setValue(code);
    }
}


export function updateMatchResponseUI(questionId, matchData) {
    const questionContainer = document.querySelector(`[data-question="${questionId}"]`);
    if (!questionContainer) {
        console.error(`Container for question ${questionId} not found`);
        return;
    }

    Object.keys(matchData.counts).forEach(leftOption => {
        const optionData = matchData.counts[leftOption];
        const totalOptionResponses = Object.values(optionData).reduce((a, b) => a + b, 0);

        Object.keys(optionData).forEach(rightOption => {
            const count = optionData[rightOption] || 0;
            const safeLeftOption = leftOption.replace(/\s+/g, '_');
            const safeRightOption = rightOption.replace(/\s+/g, '_');
            const matchRow = questionContainer.querySelector(`#match-${safeLeftOption}-${safeRightOption}`);

            if (matchRow) {
                updateProgressElements(matchRow, count, totalOptionResponses);
            }
        });
    });
}

export function updateWordCloudUI(containerID, wordData, options = {}) {
    const wordCloud = new WordCloudGenerator(containerID, options);
    wordCloud.generate(wordData);
}