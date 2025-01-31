document.addEventListener('DOMContentLoaded', function() {
    const MCAddBtn = document.getElementById('multiple-choice-add-option-btn');
    const multipleChoiceOptionsSection = document.getElementById('multiple-choice-option-section');
    let McOptionCount = multipleChoiceOptionsSection.children.length + 1;

    MCAddBtn.addEventListener('click', function() {
        console.log('Button pressed');
        const optionText=prompt('Enter a new Option');
            if (optionText){
                //create hidden input for all the options to be stored in DB otherwise only checked boxes are stored
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'multiple_choice_options[]';
                hiddenInput.value = optionText;

                const checkboxInput = document.createElement('input');
                checkboxInput.type = 'checkbox';
                checkboxInput.id = `option${McOptionCount}`;
                //only the checked inboxes will be saved as answers
                checkboxInput.name = 'multiple_choice_answers[]';
                checkboxInput.value = optionText;

                //value won't show implicitly so create a label for it
                const label = document.createElement('label');
                label.htmlFor = `option${McOptionCount}`;
                label.textContent = optionText;

                //add input to the list of option
                multipleChoiceOptionsSection.appendChild(checkboxInput);
                multipleChoiceOptionsSection.appendChild(label);
                multipleChoiceOptionsSection.appendChild(hiddenInput);

                //create a space between options
                multipleChoiceOptionsSection.appendChild(document.createTextNode(' '));

                McOptionCount++;
            }
    });

    //TO DO: add mc and sc option constraints e.g. have to pick at least one answer, has to be at least one option, only one option
    //TO DO: allow user to delete options
    //TO DO: question text must be filled

});
