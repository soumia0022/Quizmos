import {WordCloudGenerator} from "./questions/./word_cloud_generator.js";

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

export function updateResponseUI(questionId, optionCounts) {
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
    const responseListContainer = questionContainer.querySelector('.response-list-container');
    const responseList = questionContainer.querySelector(`#responseList-${questionId}`);


    responseList.innerHTML = '';

    if (responseListContainer) {
        responseListContainer.style.display = responses.length > 0 ? 'block' : 'none';
    }

    // add the responses as a list on the screen maybe update later to be able to delete
    if (responses.length <= 10) {
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

    }else {
        paginateResponses({
            container: questionContainer,
            responses,
            listSelector: `#responseList-${questionId}`,
            renderItem: (response) => {
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                listItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <span class="response-text">${response}</span>
                </div>
            `;
            responseList.appendChild(listItem);
            }
        });
    }
}

export function updateCodeResponseUI(questionId, responses, language) {
    const questionContainer = document.querySelector(`[data-question="${questionId}"]`);
    const responseList = questionContainer.querySelector(`#responseList-${questionId}`);

    responseList.innerHTML = '';

    let currentPage = 1;
    const pageSize = 10;

    function renderPage(page) {
        responseList.innerHTML = '';
        const start = (page - 1) * pageSize;
        const end = start + pageSize;
        const paginatedResponses = responses.slice(start, end);

        paginatedResponses.forEach((response) => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item';
            
            listItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <span class="response-user" style="cursor: pointer; color: blue;" data-code="${encodeURIComponent(response.code)}">
                        ${response.username}
                    </span>
                </div>
            `;
            listItem.querySelector('.response-user').addEventListener('click', function () {
                const code = decodeURIComponent(this.getAttribute('data-code'));
                displayCodeInEditor(code, language);
            });
            responseList.appendChild(listItem);
        });

        renderPaginationControls();
    }

    function renderPaginationControls() {
        const totalPages = Math.ceil(responses.length / pageSize);

        let existingContainer = questionContainer.querySelector('.pagination-controls');
        if (totalPages <= 1) {
            if (existingContainer) {
                existingContainer.remove();
            }
            return;
        }

        let paginationContainer = existingContainer
        if (!paginationContainer) {
            paginationContainer = document.createElement('div');
            paginationContainer.className = 'pagination-controls mt-2';
            questionContainer.appendChild(paginationContainer);
        }

        paginationContainer.innerHTML = `
            <button class="btn btn-sm btn-outline-primary me-2" ${currentPage === 1 ? 'disabled' : ''} id="prevPage">Previous</button>
            <span>Page ${currentPage} of ${totalPages}</span>
            <button class="btn btn-sm btn-outline-primary ms-2" ${currentPage === totalPages ? 'disabled' : ''} id="nextPage">Next</button>
        `;

        paginationContainer.querySelector('#prevPage').addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                renderPage(currentPage);
        }
        });

        paginationContainer.querySelector('#nextPage').addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                renderPage(currentPage);
            }
        });
    }


    // Show or hide response list container
    const responseListContainer = questionContainer.querySelector('.response-list-container');
    if (responseListContainer) {
        responseListContainer.style.display = responses.length > 0 ? 'block' : 'none';
    }
    renderPage(currentPage);
}

// Function to display code inside a popup(modal) with CodeMirror
function displayCodeInEditor(code, language) {
    // Remove existing modal if it exists
    let existingModal = document.getElementById('code-editor-modal');
    if (existingModal) {
        existingModal.remove();
    }

    // Create the modal container
    let modal = document.createElement('div');
    modal.id = 'code-editor-modal';
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.width = '80%';
    modal.style.maxWidth = '600px';
    modal.style.background = 'white';
    modal.style.padding = '20px';
    modal.style.borderRadius = '8px';
    modal.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    modal.style.zIndex = '1000';

    // Add a close button
    let closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '10px';
    closeButton.style.right = '10px';
    closeButton.style.background = 'red';
    closeButton.style.color = 'white';
    closeButton.style.border = 'none';
    closeButton.style.padding = '5px 10px';
    closeButton.style.cursor = 'pointer';
    closeButton.style.zIndex = '1001';
    closeButton.addEventListener('click', () => {
        modal.remove();
    });

    // Create the textarea for CodeMirror
    let textarea = document.createElement('textarea');
    textarea.id = 'code-editor';

    // Append elements to modal
    modal.appendChild(closeButton);
    modal.appendChild(textarea);
    document.body.appendChild(modal);

    // Map question.code_language to CodeMirror modes
    const languageMap = {
        "python": "text/x-python",
        "java": "text/x-java",
        "javascript": "text/javascript",
        "cpp": "text/x-c++src",
    };

    let mode = languageMap[language] || "python"; // Default to plain text if not found

    // Initialize CodeMirror
    let editor = CodeMirror.fromTextArea(textarea, {
        mode: mode,
        theme: "default",
        lineNumbers: true,
        readOnly: true // Make it read-only
    });

    // Set the retrieved code
    editor.setValue(code);
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

export {updateProgressElements}

function paginateResponses({ 
    container, 
    responses, 
    pageSize = 10, 
    renderItem, 
    listSelector, 
    paginationClass = '.pagination-controls' 
}) {
    let currentPage = 1;
    const totalPages = Math.ceil(responses.length / pageSize);

    const list = container.querySelector(listSelector);
    const paginationContainerSelector = container.querySelector(paginationClass);

    function renderPage(page) {
        list.innerHTML = '';
        const start = (page - 1) * pageSize;
        const end = start + pageSize;
        const pageItems = responses.slice(start, end);

        pageItems.forEach(renderItem);

        renderPaginationControls();
    }

    function renderPaginationControls() {
        if (totalPages <= 1) {
            if (paginationContainerSelector) paginationContainerSelector.remove();
            return;
        }

        let paginationContainer = container.querySelector(paginationClass);
        if (!paginationContainer) {
            paginationContainer.remove();
        }

        paginationContainer = document.createElement('div');
        paginationContainer.className = paginationClass.replace('.', '') + ' mt-2';
        container.appendChild(paginationContainer);

        paginationContainer.innerHTML = `
            <button class="btn btn-sm btn-outline-primary me-2" ${currentPage === 1 ? 'disabled' : ''} id="prevPage">Previous</button>
            <span>Page ${currentPage} of ${totalPages}</span>
            <button class="btn btn-sm btn-outline-primary ms-2" ${currentPage === totalPages ? 'disabled' : ''} id="nextPage">Next</button>
        `;

        paginationContainer.querySelector('#prevPage').addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                renderPage(currentPage);
            }
        });

        paginationContainer.querySelector('#nextPage').addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                renderPage(currentPage);
            }
        });
    }

    renderPage(currentPage);
}
