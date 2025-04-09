import { initializeCodeEditor, executeCode } from "./code_executor.js";

document.addEventListener('DOMContentLoaded', function () {
    const codeEditorArea = document.getElementById('code-editor');
    const runCodeButton = document.getElementById('run-code-button');
    const codingLanguageSelector = document.getElementById('coding-language-selector');

    // Language Mode Mapping
    const languageModes = {
        python: "python",
        javascript: "javascript",
        java: "text/x-java",
        cpp: "text/x-c++src"
    };

    let editor = initializeCodeEditor(codeEditorArea, languageModes[codingLanguageSelector.value], true);

    /* Event listeners */
    if (runCodeButton) {
        runCodeButton.addEventListener("click", function () {
            executeCode(editor, editor.getOption("mode"), "code-output");
        });
    }
});