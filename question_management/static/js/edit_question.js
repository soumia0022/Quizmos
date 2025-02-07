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

    deleteButtons.forEach((btn) => {
        btn.addEventListener('click', function () {
            const optionContainer = this.parentElement; // Get the div containing the option
            console.log(optionContainer.id)
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


    // TO DO: Add MC and SC option constraints (e.g., at least one answer, at least one option)
    // TO DO: Allow users to delete options
    // TO DO: Ensure question text is filled before submission
     document.querySelector('form').addEventListener('submit', function (event) {
         console.log("question type is: ", questionType)
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

});