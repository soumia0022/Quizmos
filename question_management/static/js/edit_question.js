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

    /* Event listeners*/

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

     // Dropdown Fill Preview
    dropdownInput.addEventListener('input', function() {
        originalText = dropdownInput.value // Current value is the original text - needed for resetting
        const text = dropdownInput.value;

        textPreview.innerHTML = text
            .split(' ')// Text is split into words
            .map(word => `<span class="word">${word}</span>`) // For handling each word separately
            .join(' ');
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
            dropdownQuestionText.value = dropdownInput.value;
        }
    });

     document.querySelector('form').addEventListener('submit', function (event) {
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