document.addEventListener("DOMContentLoaded", function () {
 document.querySelectorAll("[id^='correct-answer-']").forEach(function (element) {
    if (element.id.includes("options")) {
        return;
    }

    const questionId = element.id.split("-")[2];
    const pollId = document.querySelector('#pollResponsesSlideshow').dataset.pollId;
    
    fetch(`/responses/get_answer/${pollId}/${questionId}/`)
     .then(response => response.json())
     .then(data => {
        console.log(`Question ${questionId} data:`, data);
        
        if (data.correct_answer) {
            const correctAnswerContainer = document.getElementById(`correct-answer-${questionId}`);
            console.log(`Question ${questionId} answer type:`, typeof data.correct_answer, Array.isArray(data.correct_answer) ? "array" : "not array", data.correct_answer);
            
            if (Array.isArray(data.correct_answer) && data.correct_answer.length > 0 && data.correct_answer[0].left) {
                console.log(`Question ${questionId}: Handling as match question`);
                const tbody = correctAnswerContainer.querySelector('.correct-match-tbody');
                tbody.innerHTML = '';
                data.correct_answer.forEach(pair => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                     <td>${pair.left}</td>
                     <td class="bg-success text-white">${pair.right}</td>
                     `;
                    tbody.appendChild(row);
                });
            } else if (Array.isArray(data.correct_answer) && data.correct_answer.length > 0) {
                console.log(`Question ${questionId}: Handling as multiple choice`);
                const optionsContainer = document.getElementById(`correct-answer-options-${questionId}`) || correctAnswerContainer;
                optionsContainer.innerHTML = '';
                data.correct_answer.forEach(answer => {
                    const answerBox = document.createElement('div');
                    answerBox.className = 'multiple-choice-answer mb-2';
                    answerBox.innerHTML = `<p class="p-2 border rounded bg-success text-white mb-0">${answer}</p>`;
                    optionsContainer.appendChild(answerBox);
                });
            } else if (typeof data.correct_answer === 'string' && element.querySelector('code')) {
                console.log(`Question ${questionId}: Handling as code question`);
                const codeElement = correctAnswerContainer.querySelector('code');
                codeElement.textContent = data.correct_answer;
            } else if (typeof data.correct_answer === 'string') {
                console.log(`Question ${questionId}: Handling as string answer`);
                correctAnswerContainer.innerHTML = `<p class='p-2 border rounded bg-success text-white mb-0'>${data.correct_answer}</p>`;
            } else {
                console.log(`Question ${questionId}: UNHANDLED FORMAT`, data.correct_answer);
                correctAnswerContainer.innerHTML = `<p class='p-2 border rounded bg-success text-white mb-0'>${JSON.stringify(data.correct_answer)}</p>`;
            }
        } else {
            console.log(`Question ${questionId}: No correct answer available`);
            element.innerHTML = "<p class='p-2 border rounded bg-secondary text-white mb-0'>Not available</p>";
        }
     })
     .catch(error => {
        console.error(`Question ${questionId}: Error fetching:`, error);
        element.innerHTML = "<p class='p-2 border rounded bg-danger text-white mb-0'>Error loading answer</p>";
     });
 });
});