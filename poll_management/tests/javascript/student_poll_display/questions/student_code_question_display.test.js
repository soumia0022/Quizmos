import { code_question_display } from "../../../../static/js/student_poll_display/questions/code_question_display.js";
import { executeCode, initializeCodeEditor } from "../../../../static/js/code_executor.js";

jest.mock("../../../../static/js/code_executor.js");

describe("code_question_display", () => {
    let mockQuestionOptions, mockAnswerDiv, mockTextArea, mockRunButton, mockOutput;

    beforeEach(() => {
        // Mock DOM elements
        mockQuestionOptions = { innerHTML: "" };
        mockAnswerDiv = { style: { display: "block" } };
        mockTextArea = {};
        mockRunButton = { addEventListener: jest.fn() };
        mockOutput = {};

        document.getElementById = jest.fn((id) => {
            if (id === "question_options") return mockQuestionOptions;
            if (id === "answer") return mockAnswerDiv;
            if (id === "code-editor") return mockTextArea;
            if (id === "run-button") return mockRunButton;
            if (id === "output") return mockOutput;
        });

        // Mock `initializeCodeEditor` to return a fake editor instance
        initializeCodeEditor.mockReturnValue({ mockEditor: true });
    });

    it("should populate the DOM with a code editor, run button, and output display", () => {
        const data = { question: { code_language: "javascript" } };

        code_question_display(data);

        expect(mockQuestionOptions.innerHTML).toContain('<textarea id="code-editor"></textarea>');
        expect(mockQuestionOptions.innerHTML).toContain('<button id="run-button" >Run Code</button>');
        expect(mockQuestionOptions.innerHTML).toContain('<pre id="output"></pre>');

        expect(mockAnswerDiv.style.display).toBe("none");
    });

    it("should initialize the code editor with the correct language", () => {
        const data = { question: { code_language: "javascript" } };

        code_question_display(data);

        expect(initializeCodeEditor).toHaveBeenCalledWith(mockTextArea, "javascript", true);
    });

    it("should default to Python if no language is provided", () => {
        const data = { question: { code_language: null } };

        code_question_display(data);

        expect(initializeCodeEditor).toHaveBeenCalledWith(mockTextArea, "python", true);
    });

    it("should add an event listener to the run button", () => {
        const data = { question: { code_language: "python" } };

        code_question_display(data);

        expect(mockRunButton.addEventListener).toHaveBeenCalledWith(
            "click",
            expect.any(Function)
        );
    });

    it("should call executeCode when the run button is clicked", () => {
        const data = { question: { code_language: "python" } };

        code_question_display(data);

        // Get the actual event listener function that was attached to the run button
        const eventListener = mockRunButton.addEventListener.mock.calls[0][1];

        // Mock an editor instance returned by initializeCodeEditor
        const mockEditorInstance = { mockEditor: true };
        initializeCodeEditor.mockReturnValue(mockEditorInstance);

        // Simulate button click
        eventListener();

        expect(executeCode).toHaveBeenCalledWith(mockEditorInstance, "python", "output");
    });
});
