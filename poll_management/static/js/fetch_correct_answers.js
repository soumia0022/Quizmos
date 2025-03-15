    document.addEventListener("DOMContentLoaded", function () {
    function decodeUnicode(str) {
    if (!str) return '';
    return str.replace(/\\u([\dA-Fa-f]{4})/g, (match, grp) => {
    return String.fromCharCode(parseInt(grp, 16));
    });
    }

    // Function to process code elements and add line numbers
    function processCodeElement(codeElement) {
    const originalCode = codeElement.textContent;
    const decodedText = decodeUnicode(originalCode);
    const lines = decodedText.split('\n');
    codeElement.innerHTML = lines.map(line => `<span class="code-line">${line}</span>`).join('\n');
    }

    document.querySelectorAll('.code-display, .correct-code-display').forEach(processCodeElement);

    // Watch for dynamically added .correct-code-display elements
    const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
    if (mutation.addedNodes.length) {
        mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1) { 
                if (node.matches('.correct-code-display')) {
                    processCodeElement(node);
                } else {
                    node.querySelectorAll('.correct-code-display').forEach(processCodeElement);
                }
            }
        });
    }
    });
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Fetch and display correct answers
    document.querySelectorAll("[id^='correct-answer-']").forEach(function (element) {
    if (element.id.includes("options")) {
        return;
    }

    const questionId = element.id.split("-")[2];
    const pollId = document.querySelector('#pollResponsesSlideshow').dataset.pollId;
    
    fetch(`/responses/get_answer/${pollId}/${questionId}/`)
     .then(response => response.json())
     .then(data => {
        
        if (data.correct_answer) {
            const correctAnswerContainer = document.getElementById(`correct-answer-${questionId}`);

            if (data.question_type === "match_question" && Array.isArray(data.correct_answer) && data.correct_answer.length > 0 && data.correct_answer[0].left) {
                const tbody = correctAnswerContainer.querySelector('.correct-match-tbody') || document.createElement('tbody');
                tbody.classList.add('correct-match-tbody');
                tbody.innerHTML = '';
                data.correct_answer.forEach(pair => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                     <td>${pair.left}</td>
                     <td class="bg-success text-white">${pair.right}</td>
                     `;
                    tbody.appendChild(row);
                });
                if (!correctAnswerContainer.querySelector('.correct-match-tbody')) {
                    const table = document.createElement('table');
                    table.classList.add('table', 'table-bordered');
                    table.innerHTML = `
                        <thead class="bg-success text-white">
                            <tr><th>Question Item</th><th>Correct Match</th></tr>
                        </thead>
                    `;
                    table.appendChild(tbody);
                    correctAnswerContainer.innerHTML = '';
                    correctAnswerContainer.appendChild(table);
                }
            } else if ((data.question_type === "multiple_choice" || data.question_type === "single_choice") && Array.isArray(data.correct_answer) && data.correct_answer.length > 0) {
                const optionsContainer = document.getElementById(`correct-answer-options-${questionId}`) || correctAnswerContainer;
                optionsContainer.innerHTML = '';
                data.correct_answer.forEach(answer => {
                    const answerBox = document.createElement('div');
                    answerBox.className = 'multiple-choice-answer mb-2';
                    answerBox.innerHTML = `<p class="p-2 border rounded bg-success text-white mb-0">${answer}</p>`;
                    optionsContainer.appendChild(answerBox);
                });
            } 
            // Code answer
            else if (data.question_type === "code_question" && typeof data.correct_answer === 'string') {
                const codeEditorContainer = document.createElement("div");
                codeEditorContainer.classList.add("code-editor-container");

                const preElement = document.createElement("pre");
                preElement.classList.add("correct-code-display");
                preElement.textContent = data.correct_answer;

                codeEditorContainer.appendChild(preElement);
                correctAnswerContainer.innerHTML = '';
                correctAnswerContainer.appendChild(codeEditorContainer);
               
            } 
            //  string answers for remaining question types 
            else if (typeof data.correct_answer === 'string') {
                correctAnswerContainer.innerHTML = `<p class="p-2 border rounded bg-success text-white mb-0">${data.correct_answer}</p>`;
            } 
            else {
                correctAnswerContainer.innerHTML = `<p class='p-2 border rounded bg-success text-white mb-0'>${JSON.stringify(data.correct_answer)}</p>`;
            }
        } else {
            element.innerHTML = "<p class='p-2 border rounded bg-secondary text-white mb-0'>Not available</p>";
        }
     })
     .catch(error => {
        console.error(`Question ${questionId}: Error fetching:`, error);
        element.innerHTML = "<p class='p-2 border rounded bg-danger text-white mb-0'>Error loading answer</p>";
     });
 });
});