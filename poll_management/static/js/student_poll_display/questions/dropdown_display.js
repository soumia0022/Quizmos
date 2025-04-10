export function dropdown_display(data) {
    let container = document.getElementById('question_options');
    container.innerHTML = ''; 

    let dropdownWrapper = document.createElement('div');
    dropdownWrapper.classList.add('question-section'); 

    let dropdown = document.createElement('select');
    dropdown.name = "dropdown_answer";
    dropdown.classList.add("dropdown-question"); 

    let defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.innerText = "Select an option";
    dropdown.appendChild(defaultOption);

    data.question.dropdown_options.forEach(option => {
        let optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.innerText = option;
        dropdown.appendChild(optionElement);
    });

    dropdownWrapper.appendChild(dropdown);
    container.appendChild(dropdownWrapper);
    document.getElementById('answer').style.display = 'none';
}