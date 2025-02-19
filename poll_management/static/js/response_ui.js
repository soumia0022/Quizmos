//choice questions
export function updateResponseUI(questionId, optionCounts, questionType) {
    const questionContainer = document.querySelector(`[data-question="${questionId}"]`);

    const cards = questionContainer.querySelectorAll('.response-card');
    if (cards.length === 0) {
        console.error(`No response cards found for question ${questionId}`);
        return;
    }

    // Calculate total responses based on question type
    const totalResponses = Object.values(optionCounts).reduce((a, b) => a + b, 0);

    // Update each option card
    cards.forEach((card, index) => {
        const count = optionCounts[index] || 0;
        const percentage = totalResponses > 0 ? (count / totalResponses) * 100 : 0;

        const percentageElement = card.querySelector('.response-percentage');
        const countElement = card.querySelector('.response-count');
        const progressBar = card.querySelector('.progress-bar');
        const label = card.querySelector('label');

        if (percentageElement && countElement && progressBar && label) {
            percentageElement.textContent = `${percentage.toFixed(1)}%`;
            countElement.textContent = `(${count})`;
            progressBar.style.width = `${percentage}%`;
            
            // Add selected state if needed
            if (count > 0) {
                card.classList.add('has-responses');
            } else {
                card.classList.remove('has-responses');
            }
        }
    });
}


export function updateTextResponseUI(questionId, responses) {
   const questionContainer = document.querySelector(`[data-question="${questionId}"]`);
    if (!questionContainer) {
        console.error(`Container for question ${questionId} not found`);
        return;
    }

    const responseList = questionContainer.querySelector(`#responseList-${questionId}`);
    if (!responseList) {
        console.error(`Response list for question ${questionId} not found`);
        return;
    }

    // Clear existing responses
    responseList.innerHTML = '';

    // Add each response as a list item
    responses.forEach((response, index) => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span class="response-text">${response}</span>
            </div>
        `;
        responseList.appendChild(listItem);
    });

    // Show/hide the response list container based on whether there are responses
    const responseListContainer = questionContainer.querySelector('.response-list-container');
    if (responseListContainer) {
        responseListContainer.style.display = responses.length > 0 ? 'block' : 'none';
    }
}


