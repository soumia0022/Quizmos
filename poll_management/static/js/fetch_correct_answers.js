document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[id^='correct-answer-']").forEach(function (element) {
        const questionId = element.id.split("-")[2];
        const pollId = document.querySelector('#pollResponsesSlideshow').dataset.pollId;

        fetch(`/responses/get_answer/${pollId}/${questionId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.correct_answer) {
                    const correctAnswerContainer = document.getElementById(`correct-answer-${questionId}`);

                    if (Array.isArray(data.correct_answer) && data.correct_answer.length > 0 && data.correct_answer[0].left) {
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
                        const optionsContainer = document.getElementById(`correct-answer-options-${questionId}`) || correctAnswerContainer;
                        optionsContainer.innerHTML = ''; 
                    
                        data.correct_answer.forEach(answer => {
                            const answerBox = document.createElement('div');
                            answerBox.className = 'multiple-choice-answer mb-2';
                            answerBox.innerHTML = `<p class="p-2 border rounded bg-success text-white mb-0">${answer}</p>`;
                            optionsContainer.appendChild(answerBox);
                        });
                    
                    } else if (Array.isArray(data.correct_answer) && data.correct_answer.length === 0) {
                        // If correct answers exist but are empty
                        correctAnswerContainer.innerHTML = "<p class='p-2 border rounded bg-secondary text-white mb-0'>No correct answers provided</p>";
                    } else {
                        // If correct answer is missing entirely
                        correctAnswerContainer.innerHTML = "<p class='p-2 border rounded bg-danger text-white mb-0'>Error loading answer</p>";
                    }
                }
            })
            .catch(error => {
                console.error("Error fetching correct answer:", error);
                element.innerHTML = "<p class='p-2 border rounded bg-danger text-white mb-0'>Error loading answer</p>";
            });
        });
    });