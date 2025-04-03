import { displayCorrectAnswer, hideCorrectAnswer } from "../../static/js/display_correct_answer.js";
import { pollState } from "../../static/js/poll_state.js";
import { initializeCodeEditor } from "../../static/js/code_executor.js";
import { clean_up_code_mirror } from "../../static/js/clean_up_code_mirror.js";

// Mock dependencies
jest.mock("../../static/js/code_executor.js", () => ({
    initializeCodeEditor: jest.fn(() => ({
        setValue: jest.fn(),
        setOption: jest.fn(),
        refresh: jest.fn(),
    })),
}));

jest.mock("../../static/js/clean_up_code_mirror.js", () => ({
    clean_up_code_mirror: jest.fn(),
}));

describe("displayCorrectAnswer", () => {
    let correctAnswersDiv, submitButton;

    beforeEach(() => {
        // Set up a mock DOM
        document.body.innerHTML = `
            <div id="correct-answer"></div>
            <button id="submitResponse"></button>
        `;
        correctAnswersDiv = document.getElementById("correct-answer");
        submitButton = document.getElementById("submitResponse");

        pollState.currentQuestionType = null;
        pollState.currentQuestion = {};
        pollState.answerCodeEditor = null;
    });

    it("should display correct answers for multiple_choice questions", () => {
        pollState.currentQuestionType = "multiple_choice";
        const data = { answers: ["Answer A", "Answer B"] };

        displayCorrectAnswer(data, correctAnswersDiv);

        expect(correctAnswersDiv.innerHTML).toContain("<strong>Correct Answer(s):</strong> Answer A, Answer B");
        expect(correctAnswersDiv.style.display).toBe("block");
        expect(submitButton.disabled).toBe(true);
    });

    it("should display correct answer for text_fill questions", () => {
        pollState.currentQuestionType = "text_fill";
        const data = { answers: "Correct Answer" };

        displayCorrectAnswer(data, correctAnswersDiv);

        expect(correctAnswersDiv.innerHTML).toContain("<strong>Correct Answer(s):</strong> Correct Answer");
    });

    it("should display correct matches for match_question", () => {
        pollState.currentQuestionType = "match_question";
        pollState.currentQuestion.match_options = ["Option 1", "Option 2"];
        const data = { answers: ["Answer A", "Answer B"] };

        displayCorrectAnswer(data, correctAnswersDiv);

        expect(correctAnswersDiv.innerHTML).toContain("Option 1 → Answer A, Option 2 → Answer B");
    });

    it("should display 'No correct answer' for wordcloud questions", () => {
        pollState.currentQuestionType = "wordcloud";
        const data = {};

        displayCorrectAnswer(data, correctAnswersDiv);

        expect(correctAnswersDiv.innerHTML).toContain("No correct answer for word cloud.");
    });

    it("should initialize CodeMirror for code_question", () => {
        pollState.currentQuestionType = "code_question";
        pollState.currentQuestion.code_language = "javascript";
        const data = { answers: "console.log('Hello, world!');" };

        displayCorrectAnswer(data, correctAnswersDiv);

        expect(initializeCodeEditor).toHaveBeenCalled();
        expect(pollState.answerCodeEditor.setValue).toHaveBeenCalledWith("console.log('Hello, world!');");
        expect(pollState.answerCodeEditor.setOption).toHaveBeenCalledWith("readOnly", true);
    });
});

describe("hideCorrectAnswer", () => {
    let correctAnswersDiv, submitButton;

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="correct-answer" style="display: block;">Some Answer</div>
            <button id="submitResponse" disabled></button>
        `;
        correctAnswersDiv = document.getElementById("correct-answer");
        submitButton = document.getElementById("submitResponse");

        pollState.answerCodeEditor = {
            toTextArea: jest.fn(),
        };
    });

    it("should hide the correct answer and clear content", () => {
        hideCorrectAnswer(correctAnswersDiv);

        expect(correctAnswersDiv.style.display).toBe("none");
        expect(correctAnswersDiv.innerHTML).toBe("");
        expect(submitButton.disabled).toBe(false);
        expect(clean_up_code_mirror).toHaveBeenCalled();
    });
});
