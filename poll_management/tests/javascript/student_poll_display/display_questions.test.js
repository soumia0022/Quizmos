import { display_questions } from "../../../static/js/student_poll_display/display_questions.js";
import { choice_display } from "../../../static/js/student_poll_display/questions/choice_display.js";
import { dropdown_display } from "../../../static/js/student_poll_display/questions/dropdown_display.js";
import { match_display } from "../../../static/js/student_poll_display/questions/match_display.js";
import { code_question_display } from "../../../static/js/student_poll_display/questions/code_question_display.js";

// Mock all imported functions
jest.mock("../../../static/js/student_poll_display/questions/choice_display.js", () => ({
    choice_display: jest.fn(),
}));

jest.mock("../../../static/js/student_poll_display/questions/dropdown_display.js", () => ({
    dropdown_display: jest.fn(),
}));

jest.mock("../../../static/js/student_poll_display/questions/match_display.js", () => ({
    match_display: jest.fn(),
}));

jest.mock("../../../static/js/student_poll_display/questions/code_question_display.js", () => ({
    code_question_display: jest.fn(),
}));

describe("display_questions", () => {
    let mockQuestionOptions, mockAnswerDiv;

    beforeEach(() => {
        // Mock DOM elements
        mockQuestionOptions = { innerHTML: "" };
        mockAnswerDiv = { style: { display: "block" } };

        document.getElementById = jest.fn((id) => {
            if (id === "question_options") return mockQuestionOptions;
            if (id === "answer") return mockAnswerDiv;
        });
    });

    it("should call choice_display for multiple_choice questions", () => {
        const data = { question: { type: "multiple_choice" } };
        display_questions(data);
        expect(choice_display).toHaveBeenCalledWith(data, "multiple");
    });

    it("should call choice_display for single_choice questions", () => {
        const data = { question: { type: "single_choice" } };
        display_questions(data);
        expect(choice_display).toHaveBeenCalledWith(data, "single");
    });

    it("should call dropdown_display for dropdown_fill questions", () => {
        const data = { question: { type: "dropdown_fill" } };
        display_questions(data);
        expect(dropdown_display).toHaveBeenCalledWith(data);
    });

    it("should clear question_options and show answer input for text_fill questions", () => {
        const data = { question: { type: "text_fill" } };
        display_questions(data);
        expect(mockQuestionOptions.innerHTML).toBe("");
        expect(mockAnswerDiv.style.display).toBe("block");
    });

    it("should create wordcloud input fields and hide answer div for wordcloud questions", () => {
        const data = { question: { type: "wordcloud" } };
        display_questions(data);
        expect(mockQuestionOptions.innerHTML).toContain(`<input type="text" id="answer1"`);
        expect(mockQuestionOptions.innerHTML).toContain(`<input type="text" id="answer2"`);
        expect(mockAnswerDiv.style.display).toBe("none");
    });

    it("should call match_display for match_question questions", () => {
        const data = { question: { type: "match_question" } };
        display_questions(data);
        expect(match_display).toHaveBeenCalledWith(data);
    });

    it("should call code_question_display for code_question questions", () => {
        const data = { question: { type: "code_question" } };
        display_questions(data);
        expect(code_question_display).toHaveBeenCalledWith(data);
    });
});
