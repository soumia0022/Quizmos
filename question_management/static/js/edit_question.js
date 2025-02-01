document.addEventListener('DOMContentLoaded', function () {
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

    if (MCAddBtn) {
        MCAddBtn.addEventListener('click', function () {
            console.log('Button pressed');
            const optionText = prompt('Enter a new Option');
            if (optionText) {
                // Create hidden input for all options to be stored in DB (unchecked ones)
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'multiple_choice_options[]';
                hiddenInput.value = optionText;

                // Create checkbox input
                const checkboxInput = document.createElement('input');
                checkboxInput.type = 'checkbox';
                checkboxInput.id = `option${McOptionCount}`;
                checkboxInput.name = 'multiple_choice_answers[]';
                checkboxInput.value = optionText;

                // Create label for the checkbox
                const label = document.createElement('label');
                label.htmlFor = `option${McOptionCount}`;
                label.textContent = optionText;

                // Append elements to the container
                multipleChoiceOptionsSection.appendChild(checkboxInput);
                multipleChoiceOptionsSection.appendChild(label);
                multipleChoiceOptionsSection.appendChild(hiddenInput);
                multipleChoiceOptionsSection.appendChild(document.createElement('br')); // Line break for spacing

                McOptionCount++;
            }
        });
    }

    if (SCAddBtn) {
        SCAddBtn.addEventListener('click', function () {
            const optionText = prompt('Enter a new Option');
            if (optionText) {
                // Create hidden input for options
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'single_choice_options[]';
                hiddenInput.value = optionText;

                // Create checkbox input
                const checkboxInput = document.createElement('input');
                checkboxInput.type = 'checkbox';
                checkboxInput.id = `option${ScOptionCount}`;
                checkboxInput.name = 'single_choice_answers[]';
                checkboxInput.value = optionText;

                // Create label for the checkbox
                const label = document.createElement('label');
                label.htmlFor = `option${ScOptionCount}`;
                label.textContent = optionText;

                // Append elements to the container
                singleChoiceOptionsSection.appendChild(checkboxInput);
                singleChoiceOptionsSection.appendChild(label);
                singleChoiceOptionsSection.appendChild(hiddenInput);
                singleChoiceOptionsSection.appendChild(document.createElement('br')); // Line break for spacing

                ScOptionCount++;
            }
        });

    }

    if (matchQuestionAddBtn){
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
    }


    // TO DO: Add MC and SC option constraints (e.g., at least one answer, at least one option)
    // TO DO: Allow users to delete options
    // TO DO: Ensure question text is filled before submission
});