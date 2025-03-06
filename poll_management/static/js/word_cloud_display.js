export function renderWordCloud(question) {
    const questionID = question.id;
    return `<p>${question.text}</p><div id="word-cloud-${questionID}" class="word-cloud-container"></div>`;
}