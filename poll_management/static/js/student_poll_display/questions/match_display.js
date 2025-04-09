export function match_display(data) {
    let leftOptions = "";
    let rightOptions = "";

    data.question.match_options.forEach((option) => {
        leftOptions += `
            <div class="flex-container">
                <div class="match-box left">${option}</div>
                <div class="dropzone-box dropzone" data-match-target="${option}"></div>
            </div>`;
    });

    const shuffledAnswers = shuffleArray(data.question.match_answers);
    shuffledAnswers.forEach(answer => {
        rightOptions += `<div class="box draggable">${answer}</div>`;
    });

    document.getElementById('question_options').innerHTML = `
        <div class="match-container">
            ${leftOptions}
            <div id="right" class="right">
                ${rightOptions}
            </div>
        </div>`;

    document.getElementById('answer').style.display = 'none';

    initializeDragAndDrop();
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}