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
            if (!(count > 1)) {
                displayErrorMessage('Please add at least one non-correct answer for the drop down question', event);
            }
    }
});