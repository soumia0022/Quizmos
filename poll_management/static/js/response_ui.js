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
            const matchRow = questionContainer.querySelector(`#match-${leftOption}-${rightOption}`);

            if (matchRow) {
                updateProgressElements(matchRow, count, totalOptionResponses);
            }
        });
    });
}