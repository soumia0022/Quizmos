function displayErrorMessage(message, event){
    alert(message);
    event.preventDefault(); //don't allow the submission to go through
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