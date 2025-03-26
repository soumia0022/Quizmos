export function dropdown_display(data){
    let options = '<select><option value="" disabled selected>Select an option</option>';
        data.question.dropdown_options.forEach(option => {
            options += `<option value="${option}">${option}</option>`;
        });
        options += '</select>';
        document.getElementById('question_options').innerHTML = options;
        document.getElementById('answer').style.display = 'none';
}