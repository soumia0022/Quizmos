
export function updateResponseUI(questionId, optionCounts) {
    const questionContainer = document.querySelector(`[data-question="${questionId}"]`);
    if (!questionContainer) {
        console.warn(`Container for question ${questionId} not found`);
        return;
    }

    const cards = questionContainer.querySelectorAll('.response-card');
    if (cards.length === 0) {
        console.warn(`No response cards found for question ${questionId}`);
        return;
    }


    const totalResponses = Object.values(optionCounts).reduce((a, b) => a + b, 0);


    cards.forEach((card, index) => {
        const count = optionCounts[index] || 0;
        const percentage = totalResponses > 0 ? (count / totalResponses) * 100 : 0;

        const percentageElement = card.querySelector('.response-percentage');
        const countElement = card.querySelector('.response-count');
        const progressBar = card.querySelector('.progress-bar');

        if (percentageElement && countElement && progressBar) {
            percentageElement.textContent = `${percentage.toFixed(1)}%`;
            countElement.textContent = count;
            progressBar.style.width = `${percentage}%`;
        }
    });
}