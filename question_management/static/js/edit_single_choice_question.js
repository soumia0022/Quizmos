document.addEventListener('DOMContentLoaded', function () {
    const questionType = document.getElementById("question-type").value

    const SCAddBtn = document.getElementById('single-choice-add-option-btn');
    const singleChoiceOptionsSection = document.getElementById('single-choice-options-container');
    const singleChoiceOptionSetSection = document.getElementById('single-choice-option-section');

    // Ensure sections exist before counting their children
    let ScOptionCount = singleChoiceOptionSetSection ? singleChoiceOptionSetSection.children.length + 1 : 1;

    const deleteButtons = document.querySelectorAll('.delete-option-btn');

    deleteButtons.forEach((btn) => {
        btn.addEventListener('click', function () {
            const optionContainer = this.parentElement; // Get the div containing the option
            console.log(optionContainer.id)
            optionContainer.remove(); // Remove the option
        });
    });

    if (SCAddBtn) {
        SCAddBtn.addEventListener('click', function () {
            const optionText = prompt('Enter a new Option');
            if (optionText) {
                const optionContainer = document.createElement('div');
                optionContainer.className = 'single-choice-option';
                optionContainer.id = `option-container-${ScOptionCount}`;

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

                // Create delete button
                const deleteBtn = document.createElement('button');
                deleteBtn.type = 'button';
                deleteBtn.className = 'btn btn-danger btn-sm ms-2';
                deleteBtn.textContent = 'X';
                deleteBtn.addEventListener('click', function () {
                    optionContainer.remove(); // Remove the option container
                });

                // Append elements to the container
                optionContainer.appendChild(checkboxInput);
                optionContainer.appendChild(label);
                optionContainer.appendChild(hiddenInput);
                optionContainer.appendChild(deleteBtn);

                singleChoiceOptionsSection.appendChild(optionContainer);

                ScOptionCount++;
            }
        });

    }

     document.querySelector('form').addEventListener('submit', function (event) {
         console.log("question type is: ", questionType)
         if (questionType === 'single_choice'){
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
        }
    });

});