document.addEventListener('DOMContentLoaded', function() {
    // All the DOM (HTML) elements
    const addButton = document.getElementById('add-question-btn');
    const questionForm = document.getElementById('question-form');
    const questionTypeDropdown = document.getElementById('question-type-dropdown');
    const questionInputContainer = document.getElementById('question-input-container');
    const textFillFields = document.getElementById('text-fill-fields');
    const dropdownFillFields = document.getElementById('dropdown-fill-fields');


    const singleChoiceFields = document.getElementById('single-choice-fields');
    const singleChoiceOptionsSection = document.getElementById('single-choice-options-container');
    const singleChoiceAddOptionBtn = document.getElementById('single-choice-add-option-btn');
    let ScOptionCount =1;

    const multipleChoiceFields = document.getElementById('multiple-choice-fields');
    const multipleChoiceOptionsSection = document.getElementById('multiple-choice-options-container');
    const multipleChoiceAddOptionBtn = document.getElementById('multiple-choice-add-option-btn');
    let McOptionCount = 1; //must be 1 option by default

    const textFillInput = textFillFields.querySelector('input[name="text_fill_question"]');
    const dropdownQuestionInput = dropdownFillFields.querySelector('input[name="dropdown_fill_question"]');
    const dropdownOptionsInput = dropdownFillFields.querySelector('input[name="dropdown_options"]');
    const multipleChoiceInput = multipleChoiceFields.querySelector('input[name="multiple_choice_question"]');
    const singleChoiceInput = singleChoiceFields.querySelector('input[name="single_choice_question"]');
    //const singleChoiceOptionInput = singleChoiceFields.querySelector('input[name="single_choice_option"]');

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
        singleChoiceFields.style.display = 'none';
        singleChoiceInput.required = false;
        //singleChoiceOptionInput.required = false;

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
            multipleChoiceAddOptionBtn.addEventListener("click", () => {
                console.log("add option button pressed");
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
        }
    });

    document.querySelector('form').addEventListener('submit', function (event) {
    const questionType = document.getElementById('question-type-dropdown').value;

    if (questionType === 'multiple_choice'){
        const options = document.querySelectorAll('[name="multiple_choice_options[]"]');
        if (options.length === 0) {
            alert('Please add at least one option for the multiple-choice question.');
            event.preventDefault(); //don't allow the submission to go thru
        }
        const answers = document.querySelectorAll('[name="multiple_choice_answers[]"]:checked'); //only the checked ones count as answers
        if (answers.length === 0 ){
            alert('Please add at least one right answer for the multiple-choice question.');
            event.preventDefault(); //don't allow the submission to go thru
        }
    } else if (questionType === 'single_choice'){
        const options = document.querySelectorAll('[name="single_choice_options[]"]');
        if (options.length === 0) {
            alert('Please add at least one option for the single-choice question.');
            event.preventDefault(); //don't allow the submission to go thru
        }
        const answers = document.querySelectorAll('[name="single_choice_answers[]"]:checked'); //only the checked ones count as answers
        if (answers.length === 0 ){
            alert('Please add at least one right answer for the single-choice question.');
            event.preventDefault(); //don't allow the submission to go thru
        }
        else if (answers.length > 1){
            alert('You can only choose one right answer for single-choice question.');
            event.preventDefault();
        }
    }
    });

});
