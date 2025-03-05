export function renderWordCloud(question) {
    const questionID = question.id;
    return `<div id="word-cloud-${questionID}" class="word-cloud-container"></div>`;
}