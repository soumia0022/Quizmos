document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const addButton = document.getElementById('add-question-btn');
    const questionForm = document.getElementById('question-form');
    const questionTypeDropdown = document.getElementById('question-type-dropdown');
    const textFillFields = document.getElementById('text-fill-fields');
    const dropdownFillFields = document.getElementById('dropdown-fill-fields');
    const multipleChoiceFields = document.getElementById('multiple-choice-fields');
    const singleChoiceFields = document.getElementById('single-choice-fields');

    // Specifically for drop-down fill in the blank
    const dropdownInput = document.getElementById('dropdown-fill-input');
    const textPreview = document.getElementById('text-preview');
    const dropdownCorrectAnswerField = document.getElementById('dropdown-correct-answer');
    const resetButton = document.getElementById('reset-preview-btn');
    let originalText = ""; // Stores the original input text for resetting
    let blankAdded = false; // Used to only allow one blank per question

    // Show or hide the question form
    addButton.addEventListener('click', function() {
        questionForm.style.display = questionForm.style.display === 'none' ? 'block' : 'none';
    });

    // Show the correct fields based on selected question type
    questionTypeDropdown.addEventListener('change', function() {
        const questionType = questionTypeDropdown.value;

        // Hide all fields
        textFillFields.style.display = 'none';
        dropdownFillFields.style.display = 'none';
        multipleChoiceFields.style.display = 'none';
        singleChoiceFields.style.display = 'none';

        // Show the selected fields based on option selected
        if (questionType === 'text_fill') {
            textFillFields.style.display = 'block';
        } else if (questionType === 'dropdown_fill') {
            dropdownFillFields.style.display = 'block';
        } else if (questionType === 'multiple_choice') {
            multipleChoiceFields.style.display = 'block';
        } else if (questionType === 'single_choice') {
            singleChoiceFields.style.display = 'block';
        }
    });

    // Dropdown Fill Preview
    dropdownInput.addEventListener('input', function() {
        originalText = dropdownInput.value // Current value is the original text - needed for resetting
        const text = dropdownInput.value;

        textPreview.innerHTML = text
            .split(' ')// Text is split into words
            .map(word => `<span class="word">${word}</span>`) // For handling each word separately
            .join(' ');
    });

    // Handle word selection for the blank
    textPreview.addEventListener('click', function(event) { // Listener for clicks on textPreview element
        if (event.target.classList.contains('word') && !blankAdded) { // If the element clicked has class word & blank hasn't been added before
            const word = event.target.textContent; // Gets the word
            dropdownCorrectAnswerField.value = word;

            // Replace the word with a blank (this becomes the question)
            const updatedText = dropdownInput.value.replace(word, '_____');
            dropdownInput.value = updatedText;

            // Update the preview with the new text which contains the blank
            textPreview.innerHTML = updatedText
                .split(' ')
                .map(w => (w === '_____' ? `<span class="blank">_____</span>` : `<span class="word">${w}</span>`))
                .join(' ');

            blankAdded = true;
        }
    });

    // Reset Button Logic (brings back original text - sentence no longer contains a blank)
    resetButton.addEventListener('click', function() {
        dropdownInput.value = originalText; // Restore the original text
        textPreview.innerHTML = originalText
            .split(' ')
            .map(word => `<span class="word">${word}</span>`)
            .join(' ');

        // Reset to original
        dropdownCorrectAnswerField.value = "";
        blankAdded = false;
    });

    // Validation checking (for text answer and drop-down question types) below
    const form = document.querySelector('form');
    const textFillQuestionInput = document.querySelector('input[name="text_fill_question"]');
    const textFillAnswerInput = document.querySelector('input[name="text_fill_answer"]');
    const dropdownOption1Input = dropdownFillFields.querySelector('input[name="additional_options"]'); // First additional option input


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
    });

});
