// Initializes the CodeMirror editor
export function initializeCodeEditor(textarea, language = "python", displayLanguage) {
    if (!textarea) {
        console.error(`Textarea with ID '${textareaId}' not found.`);
        return null;
    }

    let modeMap = {
        python: "python",
        javascript: "javascript",
        java: "text/x-java",
        cpp: "text/x-c++src"
    };

    let commentMap = {
        python: "# This is a Python editor",
        javascript: "// This is a JavaScript editor",
        java: "// This is a Java editor",
        cpp: "// This is a C++ editor"
    };

    let editor = CodeMirror.fromTextArea(textarea, {
        mode: modeMap[language] || "python",
        theme: "default",
        lineNumbers: true
    });

    if (displayLanguage){
        // Set initial comment text
        editor.setValue(commentMap[language] || "# This is a Python editor");
    }

    return editor;
}

// Executes the code and displays the result in the specified output element
export function executeCode(editor, language, outputId) {
    if (!editor) {
        console.error("Editor instance is not available.");
        return;
    }

    const code = editor.getValue();
    let outputElement = document.getElementById(outputId);
    if (!outputElement) {
        console.error(`Output element with ID '${outputId}' not found.`);
        return;
    }

    outputElement.innerText = "Code submitted: \n" + code;
    console.log("User entered code:", code);

    // Language ID mapping for Judge0 API
    let languageIdMap = {
        python: 71,       // Python 3
        javascript: 63,   // JavaScript
        java: 62,         // Java
        cpp: 54           // C++
    };

    const data = JSON.stringify({
        source_code: btoa(code),
        language_id: languageIdMap[language] || 71,
        stdin: btoa(""),
        expected_output: "",
        cpu_time_limit: 2
    });

    console.log("Payload being sent:", data);

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === XMLHttpRequest.DONE) {
            console.log("API Response received:", this.responseText);
            try {
                const response = JSON.parse(this.responseText);

                if (response.stdout) {
                    const decodedOutput = atob(response.stdout);
                    console.log("Decoded Output:", decodedOutput);
                    outputElement.innerText = decodedOutput;
                } else if (response.stderr) {
                    const errorOutput = atob(response.stderr);
                    console.log("Error Output:", errorOutput);
                    outputElement.innerText = "Error:\n" + errorOutput;
                } else {
                    console.log("Execution failed, no output received.");
                    outputElement.innerText = "Execution failed.";
                }
            } catch (error) {
                console.error("Error parsing API response:", error);
                outputElement.innerText = "Error: Invalid API response";
            }
        }
    });

    xhr.open('POST', 'https://judge029.p.rapidapi.com/submissions?base64_encoded=true&wait=true&fields=*');
    xhr.setRequestHeader('x-rapidapi-key', '23edc00d09mshd3a835541d54666p15c81fjsnc12fc8e7ca81');
    xhr.setRequestHeader('x-rapidapi-host', 'judge029.p.rapidapi.com');
    xhr.setRequestHeader('Content-Type', 'application/json');

    console.log("Sending request to API...");
    xhr.send(data);
}
