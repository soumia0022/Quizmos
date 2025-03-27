import {initializeCodeEditor} from "./code_executor.js";
import {clean_up_code_mirror} from "./clean_up_code_mirror.js";
import {pollState} from "./poll_state.js";

export function displayCorrectAnswer(data, correctAnswersDiv) {
    const submitButton = document.getElementById("submitResponse");
    if (submitButton){
    submitButton.disabled = true;}
    let answerHtml = '<strong>Correct Answer(s):</strong> ';
    switch (pollState.currentQuestionType) {
        case 'multiple_choice':
        case 'single_choice':
            answerHtml += Array.isArray(data.answers) ? data.answers.join(', ') : data.answers;
            break;
        case 'dropdown_fill':
        case 'text_fill':
            answerHtml += data.answers;
            break;
        case 'match_question':
             const optionsArray = pollState.currentQuestion.match_options ||
                                     pollState.currentQuestion.options ||
                                     [];
                const answersArray = data.answers || data.match_answers || [];

                if (Array.isArray(answersArray) && pollState.currentQuestion && optionsArray.length > 0) {
                    answerHtml += answersArray.map((ans, idx) =>
                        `${optionsArray[idx] || ''} → ${ans}`).join(', ');
                } else {
                    answerHtml += 'Matching pairs are shown.';
                }
            break;
        case 'wordcloud':
            answerHtml += 'No correct answer for word cloud.';
            break;
        case 'code_question':
            answerHtml = '<strong>Correct Answer:</strong><div id="answer-code-display"></div>';
            correctAnswersDiv.innerHTML = answerHtml;

            // Get the code language from the current question
            let language = pollState.currentQuestion && pollState.currentQuestion.code_language ?
                pollState.currentQuestion.code_language : "python";

            // Create a textarea for the code editor
            const codeTextarea = document.createElement('textarea');
            codeTextarea.id = 'answer-code-editor';
            document.getElementById('answer-code-display').appendChild(codeTextarea);

            // Initialize CodeMirror for the answer
            pollState.answerCodeEditor = initializeCodeEditor(codeTextarea, language);

            // Set the answer code and make it read-only
            pollState.answerCodeEditor.setValue(data.answers);
            pollState.answerCodeEditor.setOption('readOnly', true);
            setTimeout(() => pollState.answerCodeEditor.refresh(), 100);
            correctAnswersDiv.style.display = 'block';
            return;
    }

    correctAnswersDiv.innerHTML = answerHtml;
    correctAnswersDiv.style.display = 'block';
}

export function hideCorrectAnswer(correctAnswersDiv) {
    correctAnswersDiv.style.display = 'none';
    correctAnswersDiv.innerHTML = '';
    const submitButton = document.getElementById("submitResponse");
    if (submitButton){
    submitButton.disabled = false;}

    clean_up_code_mirror();
}