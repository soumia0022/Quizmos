
export function choice_display(data, q_type){
    const inputType = q_type === "multiple" ? "checkbox" : "radio";
    const inputName = q_type === "multiple" ? "multiple_choice" : "single_choice";
    let options = "";
    const optionsArray = q_type === "multiple" ? data.question.mcq_options : data.question.single_option;
    optionsArray.forEach(option => {
        options += `<div><input type="${inputType}" name= "${inputName}" value="${option}"><label>${option}</label></div>`;
    });
    document.getElementById('question_options').innerHTML = options;
    document.getElementById('answer').style.display = 'none';
}