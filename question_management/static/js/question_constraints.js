function displayErrorMessage(message, event){
    alert(message);
    if (event) {
        event.preventDefault(); //don't allow the submission to go through
    }
}

function McConstraints(options, answers, questionType){
    choiceQuestionConstraints(options, answers, questionType);
}

function ScConstraints(options, answers, questionType){
    choiceQuestionConstraints(options, answers, questionType);
    if (answers.length > 1){
        displayErrorMessage('You can only choose one right answer for single-choice question.', event);
    }
}

function choiceQuestionConstraints(options, answers, questionType){
    if (options.length === 0) {
            displayErrorMessage(`Please add at least one option for the ${questionType} question.`, event);
    } else if (answers.length === 0 ){
            displayErrorMessage(`Please add at least one right answer for the ${questionType} question.`, event);
    }
}

function validateYouTubeLink(linkInput) {
    const link = typeof linkInput === 'string' ? linkInput : linkInput.value;

    const trimmedLink = link.trim().toLowerCase();

    const embedLinkRegex = /^(https?:\/\/)?(www\.)?youtube\.com\/embed\/[a-zA-Z0-9_-]+$/;
    const shortLinkRegex = /^(https?:\/\/)?(www\.)?youtu\.be\/[a-zA-Z0-9_-]+$/;

    return embedLinkRegex.test(trimmedLink) ||
           shortLinkRegex.test(trimmedLink);
}

module.exports = { displayErrorMessage, McConstraints, ScConstraints, choiceQuestionConstraints };