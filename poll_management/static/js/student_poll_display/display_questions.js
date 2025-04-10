import { choice_display } from "./questions/choice_display.js";
import { dropdown_display } from "./questions/dropdown_display.js";
import { match_display } from "./questions/match_display.js";
import { code_question_display } from "./questions/code_question_display.js";

export function display_questions(data) {
    const container = document.getElementById('question_options');
    container.innerHTML = ''; 

    let questionDiv = document.createElement('div');
    questionDiv.classList.add('card', 'question-section'); 

    
    if (data.question.type === 'multiple_choice') {
        choice_display(data, "multiple", questionDiv);

    } else if (data.question.type === 'single_choice') {
        choice_display(data, "single", questionDiv);

    } else if (data.question.type === 'dropdown_fill') {
        dropdown_display(data, questionDiv);

    } else if (data.question.type === 'text_fill') {
        document.getElementById('question_options').innerHTML = '';
        let input = document.getElementById('answer');
        
        if (input) {
            input.style.display = "block";  
            input.classList.add("text-fill-input"); 
        }
    }  else if (data.question.type === 'wordcloud') {
        let wordcloudContainer = document.createElement('div');
        wordcloudContainer.classList.add("question-section");

        let input1 = document.createElement('input');
        input1.type = "text";
        input1.id = "answer1";
        input1.name = "word_cloud_response1";
        input1.classList.add("wordcloud-input");
        input1.placeholder = "Your first answer";

        let input2 = document.createElement('input');
        input2.type = "text";
        input2.id = "answer2";
        input2.name = "word_cloud_response2";
        input2.classList.add("wordcloud-input");
        input2.placeholder = "Your second answer (optional)";

        wordcloudContainer.appendChild(input1);
        wordcloudContainer.appendChild(input2);
        container.appendChild(wordcloudContainer);

    } else if (data.question.type === 'match_question') {
        match_display(data, questionDiv);

    } else if (data.question.type === 'code_question') {
        code_question_display(data, questionDiv);
    }
}
