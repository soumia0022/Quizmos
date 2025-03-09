document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[id^='correct-answer-']").forEach(function (element) {
        const questionId = element.id.split("-")[2];
        const pollId = document.querySelector('#pollResponsesSlideshow').dataset.pollId;

        fetch(`/responses/get_answer/${pollId}/${questionId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.correct_answer) {
                    const correctAnswerDiv = document.getElementById(`correct-answer-${questionId}`);
                    if (Array.isArray(data.correct_answer) && data.correct_answer.length > 0 && data.correct_answer[0].left) {
                        const tbody = correctAnswerDiv.querySelector('.correct-match-tbody');
                        tbody.innerHTML = '';
                        data.correct_answer.forEach(pair => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${pair.left}</td>
                                <td class="bg-success text-white">${pair.right}</td>
                            `;
                            tbody.appendChild(row);
                        });
                    } else {
                        correctAnswerDiv.innerText = data.correct_answer;
                    }
                } else {
                    element.innerText = "Not available";
                }
            })
            .catch(error => console.error("Error fetching correct answer:", error));
    });
});