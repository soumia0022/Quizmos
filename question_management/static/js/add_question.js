import { initializeCodeEditor, executeCode } from "./code_executor.js";
import { addMatchOptionComponents, addMultipleChoiceOption, addSingleChoiceOption, dropdownInputChanged, resetButtonChanged, clickTextPreview } from "./question_buttons.js";
import { displayErrorMessage, ScConstraints, McConstraints, validateYouTubeLink } from "./question_constraints.js"

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const addButton = document.getElementById('add-question-btn');
    const questionForm = document.getElementById('question-form');
    const questionTypeDropdown = document.getElementById('question-type-dropdown');
    const textFillFields = document.getElementById('text-fill-fields');
    const dropdownFillFields = document.getElementById('dropdown-fill-fields');
    const wordCloudFields = document.getElementById('word-cloud-fields');

    const textFillQuestionInput = document.querySelector('input[name="text_fill_question"]');
    const textFillAnswerInput = document.querySelector('input[name="text_fill_answer"]');

    const wordCloudQuestionInput = document.querySelector('input[name="wordcloud_question"]');

    const singleChoiceFields = document.getElementById('single-choice-fields');
    const singleChoiceOptionsSection = document.getElementById('single-choice-options-container');
    const singleChoiceAddOptionBtn = document.getElementById('single-choice-add-option-btn');
    const singleChoiceInput = singleChoiceFields.querySelector('input[name="single_choice_question"]');
    let ScOptionCount =1;

    const multipleChoiceFields = document.getElementById('multiple-choice-fields');
    const multipleChoiceOptionsSection = document.getElementById('multiple-choice-options-container');
    const multipleChoiceAddOptionBtn = document.getElementById('multiple-choice-add-option-btn');
    const multipleChoiceInput = multipleChoiceFields.querySelector('input[name="multiple_choice_question"]');
    let McOptionCount = 1; //must be 1 option by default

    // Specifically for drop-down fill in the blank
    const dropdownInput = document.getElementById('dropdown-fill-input');
    const dropdownOption1Input = dropdownFillFields.querySelector('input[name="additional_options"]'); // First additional option input
    const textPreview = document.getElementById('text-preview');
    const dropdownCorrectAnswerField = document.getElementById('dropdown-correct-answer');
    const resetButton = document.getElementById('reset-preview-btn');
    let originalText = ""; // Stores the original input text for resetting
    let blankAdded = false; // Used to only allow one blank per question

    const matchQuestionFields = document.getElementById('match-fields');
    const matchQuestionOptionSection = document.getElementById('match-options-container');
    const matchQuestionAddBtn = document.getElementById('match-add-option-btn');
    const matchQuestionInput = matchQuestionFields.querySelector('input[name="match_question"]');
    let matchOptionCount = 1;

    // New Code Question fields
    const codeQuestionFields = document.getElementById('code-question-fields');
    const codeQuestionPromptInput = document.getElementById('id_code_question');
    const codeEditorArea = document.getElementById('code-editor');
    const codingLanguageSelector = document.getElementById('language-selector');
    const runCodeButton = document.getElementById('run-code-button')
    let editor = initializeCodeEditor(codeEditorArea, "python");
    // Language Mode Mapping
    const languageModes = {
        python: "python",
        javascript: "javascript",
        java: "text/x-java",
        cpp: "text/x-c++src"
    };

    /*Event Listeners */
    // Show or hide the question form
    addButton.addEventListener('click', function() {
        if (countQuestions() === 20){
            displayErrorMessage("Maximum question count reached. Cannot have more than 20 questions")
        }
        questionForm.style.display = questionForm.style.display === 'none' ? 'block' : 'none';
    });

    function countQuestions() { //move to question_constraints in refactoring
        const questionCount = document.querySelectorAll("#questions-list .question-item").length;
        // console.log("Number of questions:", questionCount);
        return questionCount;
    }

    multipleChoiceAddOptionBtn.addEventListener("click", () => {
        //function in another file, returns new McOptionCount
        McOptionCount = addMultipleChoiceOption(McOptionCount, multipleChoiceOptionsSection);
    });

    singleChoiceAddOptionBtn.addEventListener("click", () => {
        //function in another file, returns new OptionCount
       ScOptionCount = addSingleChoiceOption(ScOptionCount, singleChoiceOptionsSection)
    });

    matchQuestionAddBtn.addEventListener("click", () => {
        matchOptionCount =addMatchOptionComponents(matchQuestionOptionSection, matchOptionCount);
    });

    // Show the correct fields based on selected question type
    questionTypeDropdown.addEventListener('change', function() {
        const questionType = questionTypeDropdown.value;

        // Hide all fields
        const fields = [textFillFields, dropdownFillFields, multipleChoiceFields, singleChoiceFields, wordCloudFields, matchQuestionFields, codeQuestionFields];
        const inputFields = [multipleChoiceInput, singleChoiceInput, matchQuestionInput, textFillQuestionInput, textFillAnswerInput, wordCloudQuestionInput, dropdownOption1Input, codeQuestionPromptInput];

        fields.forEach(field => field.style.display = 'none');
        inputFields.forEach(field => field.required = false);

        //show relevant field
        showRelevantField(questionType)
    });

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
        }
    });

    codingLanguageSelector.addEventListener('change', function () {
        let selectedLanguage = this.value;
        let newMode = languageModes[selectedLanguage];

        editor.setOption("mode", newMode);
        // alert(`Mode changed to: ${newMode}`);
    });

    runCodeButton.addEventListener("click", function () {
        executeCode(editor,editor.getOption("mode"), "code-output");
    });

    function showRelevantField(questionType){
         switch (questionType) {
            case 'text_fill':
                textFillFields.style.display = 'block';
                textFillQuestionInput.required = true;
                textFillAnswerInput.required = true;
                break;
            case 'dropdown_fill':
                dropdownFillFields.style.display = 'block';
                dropdownInput.required = true;
                dropdownOption1Input.required = true;
                break;
            case 'multiple_choice':
                multipleChoiceFields.style.display = 'block';
                multipleChoiceInput.required = true;
                break;
            case 'single_choice':
                singleChoiceFields.style.display = 'block';
                singleChoiceInput.required = true;
                break;
            case 'wordcloud':
                wordCloudFields.style.display = 'block';
                wordCloudQuestionInput.required = true
                break;
            case 'match_question':
                matchQuestionFields.style.display = 'block';
                matchQuestionInput.required = true;
                break;
            case 'code_question':
                codeQuestionFields.style.display = 'block';
                codeQuestionPromptInput.required = true;
                break;
        }
    }

    // Validation checking below
    const form = document.getElementById("form");
    form.addEventListener('submit', function (event) {
        const questionType = questionTypeDropdown.value;
        const youTubeLinkInput = document.getElementById('youtube-link'); // Adjust the ID as needed
        if (youTubeLinkInput.value) {

            if(!validateYouTubeLink(youTubeLinkInput.value.trim())){
                            displayErrorMessage('Invalid YouTube link. Please use one of these formats:\n' +
                                '- Embed link: https://www.youtube.com/embed/videoID\n' +
                                '- Short link: https://youtu.be/videoID', event);
            }

        }
         if (questionType === 'multiple_choice'){
            const options = document.querySelectorAll('[name="multiple_choice_options[]"]');
            const answers = document.querySelectorAll('[name="multiple_choice_answers[]"]:checked'); //only the checked ones count as answers
            McConstraints(options, answers, 'multiple choice')
        } else if (questionType === 'single_choice'){
            const options = document.querySelectorAll('[name="single_choice_options[]"]');
            const answers = document.querySelectorAll('[name="single_choice_answers[]"]:checked'); //only the checked ones count as answers
            ScConstraints(options, answers, 'single choice')
        } else if (questionType === 'match_question'){
            const options = document.querySelectorAll('[name="match_question_options[]"]')
            if (options.length === 0) {
                displayErrorMessage('Please add at least one matching card option for the match question.', event);
            }
        } else if (questionType === 'dropdown_fill') {
            if (!dropdownCorrectAnswerField.value){
                dropdownCorrectAnswerField.style.border = '1px solid red';
                displayErrorMessage('Please fill out all required fields.', event);
            }
            else{
                dropdownCorrectAnswerField.style.border = ''; // Remove highlighting
            }
        } else if (questionType === 'code_question'){
             let codeValue = editor.getValue().trim();
             if (!codeValue){
                 displayErrorMessage("Please enter correct code", event);
             }
         }
    });

    /* This is how to do the validation testing without the required field

    // Validation checking (for text answer and drop-down question types) below
    const form = document.querySelector('form');
    const textFillQuestionInput = document.querySelector('input[name="text_fill_question"]');
    const textFillAnswerInput = document.querySelector('input[name="text_fill_answer"]');
    const dropdownOption1Input = dropdownFillFields.querySelector('input[name="additional_options"]'); // First additional option input
    const wordCloudQuestionInput = document.querySelector('input[name="wordcloud_question"]');

    // Form validation before submission without using `required` attribute
    form.addEventListener('submit', function(event) { // When the form is submitted
        const questionType = questionTypeDropdown.value;
        let isValid = true;
        let fieldsToCheck = [];

        // Fields that require an answer before saving
        if (questionType === 'text_fill') {
            fieldsToCheck = [textFillQuestionInput, textFillAnswerInput];
        } else if (questionType === 'dropdown_fill') {
            fieldsToCheck = [dropdownInput, dropdownCorrectAnswerField, dropdownOption1Input];
        } else if (questionType === 'wordcloud') {
            fieldsToCheck = [wordCloudQuestionInput]
        }

        // To check if the form is valid (so allowed to be saved)
        fieldsToCheck.forEach(function(field) {
            if (!field.value) {
                isValid = false;
                field.style.border = '1px solid red'; // Highlight the required fields
            } else {
                field.style.border = ''; // Remove highlighting
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Please fill out all required fields.');
        }
    }); */

});



