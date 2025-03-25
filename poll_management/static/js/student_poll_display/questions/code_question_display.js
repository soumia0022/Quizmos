import {executeCode, initializeCodeEditor} from "../../code_executor.js";

export function code_question_display(data){
    document.getElementById('question_options').innerHTML = `
            <textarea id="code-editor"></textarea>
            <button id="run-button" >Run Code</button>
            <pre id="output"></pre>
        `;

        document.getElementById('answer').style.display = 'none';

        let language = data.question.code_language || "python"; // Default to Python if null
        let textarea = document.getElementById('code-editor');

        let editor = initializeCodeEditor(textarea, language);

        document.getElementById('run-button').addEventListener('click', function () {
            executeCode(editor, language, 'output');
        });
}