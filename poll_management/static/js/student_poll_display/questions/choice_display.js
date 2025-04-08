import {pollState} from "../../poll_state";

export function choice_display(data, q_type) {
    const inputName = q_type === "multiple" ? "multiple_choice" : "single_choice";

    let container = document.getElementById('question_options');
    container.innerHTML = '';

    let optionsWrapper = document.createElement('div');
    optionsWrapper.classList.add('question-section');

    const selectedAnswers = new Set(); 

    const optionsArray = q_type === "multiple" ? data.question.mcq_options : data.question.single_option;
    optionsArray.forEach((option) => {
        let optionDiv = document.createElement('div');
        optionDiv.classList.add('option-item');
        optionDiv.dataset.value = option;

        let label = document.createElement('label');
        label.innerText = option;

        optionDiv.appendChild(label);
        optionsWrapper.appendChild(optionDiv);

        optionDiv.addEventListener("click", () => {
            if (q_type === "multiple") {
                if (selectedAnswers.has(option)) {
                    selectedAnswers.delete(option);
                    optionDiv.classList.remove("selected-option");
                } else {
                    selectedAnswers.add(option);
                    optionDiv.classList.add("selected-option");
                }
            } else {
                selectedAnswers.clear();
                document.querySelectorAll(".option-item").forEach(el => el.classList.remove("selected-option"));
                selectedAnswers.add(option);
                optionDiv.classList.add("selected-option");
            }
        });
    });

    container.appendChild(optionsWrapper);
    document.getElementById('answer').style.display = 'none';

    pollState.selectedAnswers = selectedAnswers;
}
