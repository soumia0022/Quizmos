document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const addButton = document.getElementById('add-question-btn');
    const questionForm = document.getElementById('question-form');
    const questionTypeDropdown = document.getElementById('question-type-dropdown');
    const textFillFields = document.getElementById('text-fill-fields');
    const dropdownFillFields = document.getElementById('dropdown-fill-fields');
    const wordCloudFields = document.getElementById('word-cloud-fields');

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
    // const codeQuestionTextInput = codeQuestionFields.querySelector('input[name="code_question_text"]');
    // const codeLanguageSelect = codeQuestionFields.querySelector('select[name="code_language"]');
    // const codeTestCasesInput = codeQuestionFields.querySelector('textarea[name="code_test_cases"]');


    
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
        multipleChoiceInput.required = false;

        singleChoiceFields.style.display = 'none';
        singleChoiceInput.required = false;

        wordCloudFields.style.display = 'none';

        matchQuestionFields.style.display = 'none';
        matchQuestionInput.required = false;

        codeQuestionFields.style.display = 'none';
        //codeQuestionTextInput.required = false;

        // Show the selected fields based on option selected
        if (questionType === 'text_fill') {
            textFillFields.style.display = 'block';
        } else if (questionType === 'dropdown_fill') {
            dropdownFillFields.style.display = 'block';
        } else if (questionType === 'multiple_choice') {
            multipleChoiceFields.style.display = 'block';
            multipleChoiceInput.required = true;
            multipleChoiceAddOptionBtn.addEventListener("click", () => {
                //console.log("add option button pressed");
                //create a new input filed for another option with placeholder text
                const optionText=prompt('Enter a new Option');
                if (optionText){
                    //create hidden input for all the options to be stored in DB otherwise only checked boxes are stored
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'multiple_choice_options[]';
                    hiddenInput.value = optionText;

                    const checkboxInput = document.createElement('input');
                    checkboxInput.type = 'checkbox';
                    checkboxInput.id = `option${McOptionCount}`;
                    //only the checked inboxes will be saved as answers
                    checkboxInput.name = 'multiple_choice_answers[]';
                    checkboxInput.value = optionText;

                    //value won't show implicitly so create a label for it
                    const label = document.createElement('label');
                    label.htmlFor = `option${McOptionCount}`;
                    label.textContent = optionText;

                    //add input to the list of option
                    multipleChoiceOptionsSection.appendChild(checkboxInput);
                    multipleChoiceOptionsSection.appendChild(label);
                    multipleChoiceOptionsSection.appendChild(hiddenInput);

                    //create a space between options
                    multipleChoiceOptionsSection.appendChild(document.createTextNode(' '));
                    McOptionCount++;
                }
            });
        } else if (questionType === 'single_choice') {
            singleChoiceFields.style.display = 'block';
            singleChoiceInput.required = true;
            singleChoiceAddOptionBtn.addEventListener("click", () => {
                //create a new input filed for another option with placeholder text
                const optionText=prompt('Enter a new Option');
                if (optionText){
                    //create hidden input for all the options to be stored in DB otherwise only checked boxes are stored
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'single_choice_options[]';
                    hiddenInput.value = optionText;

                    const checkboxInput = document.createElement('input');
                    checkboxInput.type = 'checkbox';
                    checkboxInput.id = `option${ScOptionCount}`;
                    //only the checked inboxes will be saved as answers
                    checkboxInput.name = 'single_choice_answers[]';
                    checkboxInput.value = optionText;

                    //value won't show implicitly so create a label for it
                    const label = document.createElement('label');
                    label.htmlFor = `option${ScOptionCount}`;
                    label.textContent = optionText;

                    //add input to the list of option
                    singleChoiceOptionsSection.appendChild(checkboxInput);
                    singleChoiceOptionsSection.appendChild(label);
                    singleChoiceOptionsSection.appendChild(hiddenInput);

                    //create a space between options
                    singleChoiceOptionsSection.appendChild(document.createTextNode(' '));
                    ScOptionCount++;
                }
            });
        } else if (questionType === "wordcloud") {
            wordCloudFields.style.display = 'block';
        } else if (questionType === 'match_question') {
            matchQuestionFields.style.display = 'block';
            matchQuestionInput.required = true;
            matchQuestionAddBtn.addEventListener("click", () => {
                const inputRow = document.createElement("div");

                const option = document.createElement("input");
                option.type = "text";
                option.placeholder = `Option ${matchOptionCount}`;
                option.name = 'match_question_options[]';
                option.required = true;

                const answer = document.createElement("input");
                answer.type = "text";
                answer.placeholder = `Answer ${matchOptionCount}`;
                answer.name = 'match_question_answers[]';
                answer.required = true;

                inputRow.appendChild(option);
                inputRow.appendChild(answer)

                matchQuestionOptionSection.appendChild(inputRow);
                matchOptionCount++;
            });
        } else if (questionType === 'code_question') {
            codeQuestionFields.style.display = 'block';
        }
    });

    document.querySelector('form').addEventListener('submit', function (event) {
    const questionType = document.getElementById('question-type-dropdown').value;

    if (questionType === 'multiple_choice'){
        const options = document.querySelectorAll('[name="multiple_choice_options[]"]');
        if (options.length === 0) {
            alert('Please add at least one option for the multiple-choice question.');
            event.preventDefault(); //don't allow the submission to go through
        }
        const answers = document.querySelectorAll('[name="multiple_choice_answers[]"]:checked'); //only the checked ones count as answers
        if (answers.length === 0 ){
            alert('Please add at least one right answer for the multiple-choice question.');
            event.preventDefault(); //don't allow the submission to go through
        }
    } else if (questionType === 'single_choice'){
        const options = document.querySelectorAll('[name="single_choice_options[]"]');
        if (options.length === 0) {
            alert('Please add at least one option for the single-choice question.');
            event.preventDefault(); //don't allow the submission to go through
        }
        const answers = document.querySelectorAll('[name="single_choice_answers[]"]:checked'); //only the checked ones count as answers
        if (answers.length === 0 ){
            alert('Please add at least one right answer for the single-choice question.');
            event.preventDefault(); //don't allow the submission to go through
        }
        else if (answers.length > 1){
            alert('You can only choose one right answer for single-choice question.');
            event.preventDefault();
        }
    } else if (questionType === 'match_question'){
        const options = document.querySelectorAll('[name="match_question_options[]"]')
        if (options.length === 0) {
            alert('Please add at least one matching card option for the match question.');
            event.preventDefault(); //don't allow the submission to go thru
        }
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
    });

});
