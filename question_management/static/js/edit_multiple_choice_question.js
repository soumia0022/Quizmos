document.addEventListener('DOMContentLoaded', function () {
    const questionType = document.getElementById("question-type").value

    const MCAddBtn = document.getElementById('multiple-choice-add-option-btn');
    const multipleChoiceOptionsSection = document.getElementById('multiple-choice-options-container');
    const multipleChoiceOptionsSetSection = document.getElementById('multiple-choice-option-section');

    // Ensure sections exist before counting their children
    let McOptionCount = multipleChoiceOptionsSetSection ? multipleChoiceOptionsSetSection.children.length + 1 : 1;

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
            console.log('Button pressed');
            const optionText = prompt('Enter a new Option');
            if (optionText) {
                const optionContainer = document.createElement('div');
                optionContainer.className = 'multiple-choice-option';
                optionContainer.id = `option-container-${McOptionCount}`;

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

                multipleChoiceOptionsSection.appendChild(optionContainer);
                McOptionCount++;
            }
        });
    }
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
        }
    });
});