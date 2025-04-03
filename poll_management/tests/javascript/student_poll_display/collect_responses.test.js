import { collectResponse } from "../../../static/js/student_poll_display/collect_responses.js";
import { pollState } from "../../../static/js/poll_state.js";
import { showFeedback } from "../../../static/js/student_poll_display/show_feedback.js";

// Mock showFeedback function
jest.mock("../../../static/js/student_poll_display/show_feedback.js", () => ({
    showFeedback: jest.fn(),
}));

describe("collectResponse", () => {
    beforeEach(() => {
        // Reset mocks before each test
        jest.clearAllMocks();
        document.body.innerHTML = ""; // Reset DOM
    });

    it("should return selected values for multiple choice", () => {
        pollState.currentQuestionType = 'multiple_choice';
        document.body.innerHTML = `
            <input type="checkbox" value="Option 1" checked>
            <input type="checkbox" value="Option 2" checked>
        `;

        const response = collectResponse();
        expect(response).toEqual(["Option 1", "Option 2"]);
    });

    it("should return selected value for single choice", () => {
        pollState.currentQuestionType = 'single_choice';
        document.body.innerHTML = `
            <input type="radio" name="single_choice" value="Option A">
            <input type="radio" name="single_choice" value="Option B" checked>
        `;

        const response = collectResponse();
        expect(response).toBe("Option B");
    });

    it("should return selected value for dropdown fill", () => {
        pollState.currentQuestionType = 'dropdown_fill';
        document.body.innerHTML = `
            <select>
                <option value="Option 1">Option 1</option>
                <option value="Option 2" selected>Option 2</option>
            </select>
        `;

        const response = collectResponse();
        expect(response).toBe("Option 2");
    });

    it("should return text input value for text fill", () => {
        pollState.currentQuestionType = 'text_fill';
        document.body.innerHTML = `<input type="text" id="answer" value="User input">`;

        const response = collectResponse();
        expect(response).toBe("User input");
    });

    it("should return matched data for match question", () => {
        pollState.currentQuestionType = 'match_question';
        document.body.innerHTML = `
            <div class="flex-container">
                <div class="left">Option A</div>
                <div class="dropzone">
                    <div class="box">Answer 1</div>
                </div>
            </div>
        `;

        const response = collectResponse();
        expect(response).toEqual([{ left: "Option A", right: "Answer 1" }]);
        expect(showFeedback).not.toHaveBeenCalled();
    });

    it("should call showFeedback if match data is incomplete", () => {
        pollState.currentQuestionType = 'match_question';
        document.body.innerHTML = `
            <div class="flex-container">
                <div class="left">Option A</div>
                <div class="dropzone"></div>
            </div>
        `;

        const response = collectResponse();
        expect(response).toBeNull();
        expect(showFeedback).toHaveBeenCalledWith('Please match all items before submitting.', false);
    });

    it("should return filtered wordcloud answers", () => {
        pollState.currentQuestionType = 'wordcloud';
        document.body.innerHTML = `
            <input type="text" id="answer1" value="Word 1">
            <input type="text" id="answer2" value="">
        `;

        const response = collectResponse();
        expect(response).toEqual(["Word 1"]);
    });

    it("should return code editor value for code question", () => {
        pollState.currentQuestionType = 'code_question';
        document.body.innerHTML = `<div class="CodeMirror"></div>`;

        const mockEditor = {
            getValue: jest.fn().mockReturnValue("console.log('Hello World');"),
        };
        document.querySelector = jest.fn().mockReturnValue({ CodeMirror: mockEditor });

        const response = collectResponse();
        expect(response).toBe("console.log('Hello World');");
    });
});
