import {showFeedback} from "./show_feedback.js";
import {pollState} from "../poll_state.js";

export function collectResponse() {
    switch (pollState.currentQuestionType) {
        case 'multiple_choice':
            return Array.from(document.querySelectorAll('.option-item.selected-option'))
                .map(option => option.dataset.value);

        case 'single_choice':
            const selectedOption = document.querySelector('.option-item.selected-option');
            return selectedOption ? selectedOption.dataset.value : null;

        case 'dropdown_fill':
            const selectedDropdown = document.querySelector('select');
            return selectedDropdown ? selectedDropdown.value : null;

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
            }
    }
    return null;
}