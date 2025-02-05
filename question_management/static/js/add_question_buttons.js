function addMultipleChoiceOption(McOptionCount, multipleChoiceOptionsSection) {
    multipleChoiceOptionsSection.appendChild(addOptionComponents('multiple_choice', McOptionCount));
    return McOptionCount + 1;
}

function addSingleChoiceOption(ScOptionCount, singleChoiceOptionsSection) {
    singleChoiceOptionsSection.appendChild(addOptionComponents('single_choice', ScOptionCount));
    return ScOptionCount + 1; // Increment and return the updated count
}

function addOptionComponents(question_type, optionCount){
    const optionText = prompt('Enter a new Option');
    if (!optionText) return;

    const optionContainer = document.createElement('div');
    optionContainer.className = 'single-choice-option';
    optionContainer.id = `option-container-${optionCount}`;

    // Create hidden input for options
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = `${question_type}_options[]`;
    hiddenInput.value = optionText;

    // Create checkbox input
    const checkboxInput = document.createElement('input');
    checkboxInput.type = 'checkbox';
    checkboxInput.id = `option${optionCount}`;
    checkboxInput.name = `${question_type}_answers[]`;
    checkboxInput.value = optionText;

    // Create label for the checkbox
    const label = document.createElement('label');
    label.htmlFor = `option${optionCount}`;
    label.textContent = optionText;

    // Add a delete button if needed
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

    return optionContainer;
}