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
    McOptionCount++;
}