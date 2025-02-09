function addMultipleChoiceOption(McOptionCount, multipleChoiceOptionsSection) {
    multipleChoiceOptionsSection.appendChild(addChoiceOptionComponents('multiple_choice', McOptionCount));
    return McOptionCount + 1;
}

function addSingleChoiceOption(ScOptionCount, singleChoiceOptionsSection) {
    singleChoiceOptionsSection.appendChild(addChoiceOptionComponents('single_choice', ScOptionCount));
    return ScOptionCount + 1; // Increment and return the updated count
}

function addChoiceOptionComponents(question_type, optionCount){
    const optionText = prompt('Enter a new Option');
    if (!optionText) return;

    const optionContainer = document.createElement('div');
    optionContainer.className = `${question_type}-option`;
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
    deleteBtn.className = 'btn btn-danger btn-sm ms-2 delete-option-btn';
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

function addMatchOptionComponents(matchQuestionOptionSection, matchOptionCount){
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

    // Create delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.className = 'btn btn-danger btn-sm ms-2';
    deleteBtn.textContent = 'X';
    deleteBtn.addEventListener('click', function () {
        inputRow.remove(); // Remove the option container
        matchOptionCount--;
    });

    inputRow.appendChild(option);
    inputRow.appendChild(answer)
    inputRow.appendChild(deleteBtn)

    matchQuestionOptionSection.appendChild(inputRow);
    return matchOptionCount+1;
}

function dropdownInputChanged(originalText, textPreview, dropdownInput){
     originalText = dropdownInput.value // Current value is the original text - needed for resetting
    const text = dropdownInput.value;

    textPreview.innerHTML = text
        .split(' ')// Text is split into words
        .map(word => `<span class="word">${word}</span>`) // For handling each word separately
        .join(' ');
}

function resetButtonChanged(dropdownInput, textPreview, originalText, dropdownCorrectAnswerField){
    dropdownInput.value = originalText; // Restore the original text
    textPreview.innerHTML = originalText
        .split(' ')
        .map(word => `<span class="word">${word}</span>`)
        .join(' ');

    // Reset to original
    dropdownCorrectAnswerField.value = "";
}

function clickTextPreview(dropdownCorrectAnswerField, dropdownInput, textPreview){
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
}