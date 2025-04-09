import { executeCode, initializeCodeEditor } from "../../code_executor.js";

export function code_question_display(data){
    document.getElementById('question_options').innerHTML = `
        <div class="code-question-wrapper">
            <div class="code-editor-container">
                <textarea id="code-editor"></textarea>
                <button id="run-button">Run Code</button>
            </div>
            <div class="output-header">Output:</div>
            <pre id="output"></pre>
        </div>
    `;

    document.getElementById('answer').style.display = 'none';

    let language = data.question.code_language || "python"; // Default to Python if null
    let textarea = document.getElementById('code-editor');

    let editor = initializeCodeEditor(textarea, language, true);

    document.getElementById('run-button').addEventListener('click', function () {
        executeCode(editor, language, 'output');
    });
}
