import {choice_display} from "./questions/choice_display.js";
import {dropdown_display} from "./questions/dropdown_display.js";
import {match_display} from "./questions/match_display.js";
import {code_question_display} from "./questions/code_question_display.js";

export function display_questions(data){

    if (data.question.type === 'multiple_choice') {
        choice_display(data, "multiple");

    } else if (data.question.type === 'single_choice') {
        choice_display(data, "single")
    } else if (data.question.type === 'dropdown_fill') {
        dropdown_display(data);

    } else if (data.question.type === 'text_fill') {
        document.getElementById('question_options').innerHTML = '';
        document.getElementById('answer').style.display = 'block';

    } else if (data.question.type === 'wordcloud') {
        document.getElementById('question_options').innerHTML = `
            <input type="text" id="answer1" name="word_cloud_response1" placeholder="Your first answer" />
            <input type="text" id="answer2" name="word_cloud_response2" placeholder="Your second answer (optional)" />`;
        document.getElementById('answer').style.display = 'none';

    } else if (data.question.type === 'match_question') {
        match_display(data);
    }
    else if (data.question.type === 'code_question') {
        code_question_display(data);
}}

