import {initializeCodeEditor, executeCode} from "../code_executor.js";
import {choice_display} from "./questions/choice_display.js";

export function display_questions(data){

    if (data.question.type === 'multiple_choice') {
        choice_display(data, "multiple");

    } else if (data.question.type === 'single_choice') {
        choice_display(data, "single")
    } else if (data.question.type === 'dropdown_fill') {
        let options = '<select><option value="" disabled selected>Select an option</option>';
        data.question.dropdown_options.forEach(option => {
            options += `<option value="${option}">${option}</option>`;
        });
        options += '</select>';
        document.getElementById('question_options').innerHTML = options;
        document.getElementById('answer').style.display = 'none';

    } else if (data.question.type === 'text_fill') {
        document.getElementById('question_options').innerHTML = '';
        document.getElementById('answer').style.display = 'block';

    } else if (data.question.type === 'wordcloud') {
        document.getElementById('question_options').innerHTML = `
            <input type="text" id="answer1" name="word_cloud_response1" placeholder="Your first answer" />
            <input type="text" id="answer2" name="word_cloud_response2" placeholder="Your second answer (optional)" />`;
        document.getElementById('answer').style.display = 'none';

    } else if (data.question.type === 'match_question') {
        let leftOptions = "";
        let rightOptions = "";

        data.question.match_options.forEach((option) => {
            leftOptions += `
                <div class="flex-container">
                    <div class="box left">${option}</div>
                    <div class="dropzone-box dropzone"></div>
                </div>`;
        });

        const shuffledAnswers = shuffleArray(data.question.match_answers);
        shuffledAnswers.forEach(answer => {
            rightOptions += `<div class="box draggable">${answer}</div>`;
        });

        document.getElementById('question_options').innerHTML = `
            <div class="container">
                ${leftOptions}
               <div id="right" class="right">
                    ${rightOptions}
                </div>
            </div>`;

        document.getElementById('answer').style.display = 'none';

        initializeDragAndDrop();
        initializeSortable();
    } else if (data.question.type === 'code_question') {
        document.getElementById('question_options').innerHTML = `
            <textarea id="code-editor"></textarea>
            <button id="run-button" >Run Code</button>
            <pre id="output"></pre>
        `;

        document.getElementById('answer').style.display = 'none';

        let language = data.question.code_language || "python"; // Default to Python if null
        let textarea = document.getElementById('code-editor');

        // Initialize CodeMirror using imported function
        let editor = initializeCodeEditor(textarea, language);

        document.getElementById('run-button').addEventListener('click', function () {
            executeCode(editor, language, 'output'); // Use imported function
        });
}}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}