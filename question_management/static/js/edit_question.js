import { initializeCodeEditor, executeCode } from "./code_executor.js";
import {
    addMatchOptionComponents,
    addMultipleChoiceOption,
    addSingleChoiceOption, clickTextPreview,
    dropdownInputChanged, resetButtonChanged
} from "./question_buttons.js";
import {displayErrorMessage, McConstraints, ScConstraints} from "./question_constraints.js";

document.addEventListener('DOMContentLoaded', function () {
    const questionType = document.getElementById("question-type").value

    const MCAddBtn = document.getElementById('multiple-choice-add-option-btn');
    const multipleChoiceOptionsSection = document.getElementById('multiple-choice-options-container');
    const multipleChoiceOptionsSetSection = document.getElementById('multiple-choice-option-section');

    const SCAddBtn = document.getElementById('single-choice-add-option-btn');
    const singleChoiceOptionsSection = document.getElementById('single-choice-options-container');
    const singleChoiceOptionSetSection = document.getElementById('single-choice-option-section');

    const matchQuestionOptionSection = document.getElementById('match-options-container');
    const matchQuestionSetSection = document.getElementById('match-pre-filled-options')
    const matchQuestionAddBtn = document.getElementById('match-add-option-btn');

    const dropdownQuestionText = document.getElementById('dropdown-question-text')
    const dropdownInput = document.getElementById('dropdown-fill-input');
    const textPreview = document.getElementById('text-preview');
    const dropdownCorrectAnswerField = document.getElementById('dropdown-correct-answer');
    const resetButton = document.getElementById('reset-preview-btn');
    let originalText = ""; // Stores the original input text for resetting
    let blankAdded = false; // Used to only allow one blank per question

    // Ensure sections exist before counting their children
    let McOptionCount = multipleChoiceOptionsSetSection ? multipleChoiceOptionsSetSection.children.length + 1 : 1;
    let ScOptionCount = singleChoiceOptionSetSection ? singleChoiceOptionSetSection.children.length + 1 : 1;
    //Check to make sure the first 2 ones are working properly
    let matchOptionCount = matchQuestionSetSection ? (matchQuestionSetSection.children.length) : 1;

    //for the delete buttons that appear with the pre-existing data
    const deleteButtons = document.querySelectorAll('.delete-option-btn');

    const codingLanguageSelector = document.getElementById('language-selector');
    const codeEditorArea = document.getElementById('code-editor');
    const runCodeButton = document.getElementById('run-code-button')
    let editor = initializeCodeEditor(codeEditorArea, "python");
    // Language Mode Mapping
    const languageModes = {
        python: "python",
        javascript: "javascript",
        java: "text/x-java",
        cpp: "text/x-c++src"
    };

    /* Event listeners*/
    if (runCodeButton) {
        runCodeButton.addEventListener("click", function () {
            executeCode(editor, editor.getOption("mode"), "code-output");
        });
    }

    if (codingLanguageSelector) {
        codingLanguageSelector.addEventListener('change', function () {
            let selectedLanguage = this.value;
            let newMode = languageModes[selectedLanguage];

            editor.setOption("mode", newMode);
            // alert(`Mode changed to: ${newMode}`);
        });
    }

    deleteButtons.forEach((btn) => {
        btn.addEventListener('click', function () {
            const optionContainer = this.parentElement; // Get the div containing the option
            optionContainer.remove(); // Remove the option
        });
    });

    if (MCAddBtn) {
        MCAddBtn.addEventListener('click', function () {
            addMultipleChoiceOption(McOptionCount, multipleChoiceOptionsSection);
        });
    }

    if (SCAddBtn) {
        SCAddBtn.addEventListener('click', function () {
            addSingleChoiceOption(ScOptionCount, singleChoiceOptionsSection)
        });

    }

    if (matchQuestionAddBtn){
        matchQuestionAddBtn.addEventListener("click", () => {
            matchOptionCount = addMatchOptionComponents(matchQuestionOptionSection, matchOptionCount);
        });
    }

    if (dropdownInput) {
        // Dropdown Fill Preview
        dropdownInput.addEventListener('input', function() {
            originalText = dropdownInputChanged(originalText, textPreview, dropdownInput);
        });

            // Reset Button Logic (brings back original text - sentence no longer contains a blank)
        resetButton.addEventListener('click', function() {
            resetButtonChanged(dropdownInput, textPreview, originalText, dropdownCorrectAnswerField)
            blankAdded = false;
        });

            // Handle word selection for the blank
        textPreview.addEventListener('click', function(event) { // Listener for clicks on textPreview element
            if (event.target.classList.contains('word') && !blankAdded) { // If the element clicked has class word & blank hasn't been added before
                clickTextPreview(dropdownCorrectAnswerField,dropdownInput,textPreview);
                blankAdded = true;
                dropdownQuestionText.value = dropdownInput.value;
            }
        });
    }

    const form = document.querySelectorAll('form')[1];
    form.addEventListener('submit', function (event) {
        if (questionType === 'multiple_choice'){
            const options = document.querySelectorAll('[name="multiple_choice_options[]"]');
            const answers = document.querySelectorAll('[name="multiple_choice_answers[]"]:checked'); //only the checked ones count as answers
            McConstraints(options, answers, 'multiple choice')
        } else if (questionType === 'single_choice'){
            const options = document.querySelectorAll('[name="single_choice_options[]"]');
            const answers = document.querySelectorAll('[name="single_choice_answers[]"]:checked'); //only the checked ones count as answers
            ScConstraints(options, answers, 'single choice')
        } else if (questionType === 'match_question'){
            const options = document.querySelectorAll('[name="match_question_options[]"]');
            if (options.length === 0) {
                displayErrorMessage('Please add at least one matching card option for the match question.', event);
            }
        } else if (questionType === 'dropdown_fill'){
            const options = document.querySelectorAll('[name="dropdown_options[]"]');
            dropdownConstraint(options);
        } else if (questionType === 'code_question'){
             let codeValue = editor.getValue().trim();
             if (!codeValue){
                 displayErrorMessage("Please enter correct code", event);
             }
        }
    });

    function dropdownConstraint(options){
         let count = 0;
            options.forEach(option => {
                if (option.value.trim() !== '') {
                    count++;
                }
            });
            console.log(count);
            if (!(count > 0)) {
                displayErrorMessage('Please add at least one non-correct answer for the drop down question', event);
            }
    }
});