document.addEventListener('DOMContentLoaded', function() {

    // All the DOM (HTML) elements
    const addButton = document.getElementById('add-question-btn');
    const questionForm = document.getElementById('question-form');
    const questionTypeDropdown = document.getElementById('question-type-dropdown');
    const questionInputContainer = document.getElementById('question-input-container');
    const textFillFields = document.getElementById('text-fill-fields');
    const dropdownFillFields = document.getElementById('dropdown-fill-fields');
    const multipleChoiceFields = document.getElementById('multiple-choice-fields');
    const singleChoiceFields = document.getElementById('single-choice-fields');

    const textFillInput = textFillFields.querySelector('input[name="text_fill_question"]');
    const dropdownQuestionInput = dropdownFillFields.querySelector('input[name="dropdown_fill_question"]');
    const dropdownOptionsInput = dropdownFillFields.querySelector('input[name="dropdown_options"]');
    const multipleChoiceInput = multipleChoiceFields.querySelector('input[name="multiple_choice_question"]');
    const multipleChoiceOptionsInput = multipleChoiceFields.querySelector('input[name="multiple_choice_options"]');
    const singleChoiceInput = singleChoiceFields.querySelector('input[name="single_choice_question"]');
    const singleChoiceOptionInput = singleChoiceFields.querySelector('input[name="single_choice_option"]');

    // Show or hide the question form when clicking the "Add Question" button
    addButton.addEventListener('click', function() {
        questionForm.style.display = questionForm.style.display === 'none' ? 'block' : 'none';
    });

    // Show question input field only after selecting a question type
    questionTypeDropdown.addEventListener('change', function() {
        const questionType = questionTypeDropdown.value;

        // Hide all question formats and remove the "required" attribute
        textFillFields.style.display = 'none';
        textFillInput.required = false;
        dropdownFillFields.style.display = 'none';
        dropdownQuestionInput.required = false;
        dropdownOptionsInput.required = false;
        multipleChoiceFields.style.display = 'none';
        multipleChoiceInput.required = false;
        multipleChoiceOptionsInput.required = false;
        singleChoiceFields.style.display = 'none';
        singleChoiceInput.required = false;
        singleChoiceOptionInput.required = false;

        // Show the relevant question format based on selected type and add the "required" attribute
        if (questionType === 'text_fill') {
            textFillFields.style.display = 'block';
            textFillInput.required = true;
        } else if (questionType === 'dropdown_fill') {
            dropdownFillFields.style.display = 'block';
            dropdownQuestionInput.required = true;
            dropdownOptionsInput.required = true;
        } else if (questionType === 'multiple_choice') {
            multipleChoiceFields.style.display = 'block';
            multipleChoiceInput.required = true;
            multipleChoiceOptionsInput.required = true;
        } else if (questionType === 'single_choice') {
            singleChoiceFields.style.display = 'block';
            singleChoiceInput.required = true;
            singleChoiceOptionInput.required = true;
        }
    });
});
