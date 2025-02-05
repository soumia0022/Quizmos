function addMultipleChoiceOption(McOptionCount, multipleChoiceOptionsSection) {
    const optionText = prompt('Enter a new Option');
    if (!optionText) return;

    const optionContainer = document.createElement('div');
    optionContainer.className = 'multiple-choice-option';
    optionContainer.id = `option-container-${McOptionCount}`;

    // Hidden input (stores unchecked options)
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'multiple_choice_options[]';
    hiddenInput.value = optionText;

    // Checkbox input
    const checkboxInput = document.createElement('input');
    checkboxInput.type = 'checkbox';
    checkboxInput.id = `option${McOptionCount}`;
    checkboxInput.name = 'multiple_choice_answers[]';
    checkboxInput.value = optionText;

    // Label
    const label = document.createElement('label');
    label.htmlFor = `option${McOptionCount}`;
    label.textContent = optionText;

    // Delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.className = 'btn btn-danger btn-sm ms-2';
    deleteBtn.textContent = 'X';
    deleteBtn.addEventListener('click', function () {
        optionContainer.remove(); // Remove option
    });

    // Append elements
    optionContainer.appendChild(checkboxInput);
    optionContainer.appendChild(label);
    optionContainer.appendChild(hiddenInput);
    optionContainer.appendChild(deleteBtn);

    multipleChoiceOptionsSection.appendChild(optionContainer);
    return McOptionCount + 1;
}

function addSingleChoiceOption(ScOptionCount, singleChoiceOptionsSection) {
    const optionText = prompt('Enter a new Option');
    if (!optionText) return;

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
    singleChoiceOptionsSection.appendChild(optionContainer);

    return ScOptionCount + 1; // Increment and return the updated count
}

