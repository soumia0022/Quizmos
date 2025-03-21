import {showFeedback} from "./show_feedback.js";

export function collectResponse(pollState) {
    switch (pollState.currentQuestionType) {
        case 'multiple_choice':
            return Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                .map(cb => cb.value);
        case 'single_choice':
            const selectedRadio = document.querySelector('input[name="single_choice"]:checked');
            return selectedRadio ? selectedRadio.value : null;
        case 'dropdown_fill':
            const selectedOption = document.querySelector('select').value;
            return selectedOption || null;
        case 'text_fill':
            return document.getElementById('answer').value;
        case 'match_question':
            const matchData = Array.from(document.querySelectorAll('.flex-container')).map(container => {
                const leftOption = container.querySelector('.left').textContent.trim();
                const rightOptionElement = container.querySelector('.dropzone .box');
                const rightOption = rightOptionElement ? rightOptionElement.textContent.trim() : null;
                return {
                    left: leftOption,
                    right: rightOption
                };
            });
            if (matchData.some(match => !match.right)) {
                showFeedback('Please match all items before submitting.', false);
                return null;
            }
            return matchData;
        case 'wordcloud':
            const answer1 = document.getElementById('answer1').value;
            const answer2 = document.getElementById('answer2').value;
            return [answer1, answer2].filter(answer => answer !== '');
        case 'code_question':
            // Get the CodeMirror instance from the text area
            let codeEditor = document.querySelector('.CodeMirror'); // Get the CodeMirror container
            if (codeEditor) {
                let editorInstance = codeEditor.CodeMirror; // Access CodeMirror instance
                return editorInstance.getValue(); // Get the code inside the editor
            } else {
                console.error("CodeMirror instance not found.");
                return "";
            }}
    return null;
}