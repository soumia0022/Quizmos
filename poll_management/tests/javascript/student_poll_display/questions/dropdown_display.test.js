import { dropdown_display } from "../../../../static/js/student_poll_display/questions/dropdown_display.js";

describe("dropdown_display", () => {
    let mockQuestionOptions, mockAnswerDiv;

    beforeEach(() => {
        // Mock DOM elements
        mockQuestionOptions = {
            innerHTML: "",
            appendChild: jest.fn(function (child) {
                this.innerHTML += child.outerHTML; // Simulating real appendChild
            }),
        };

        mockAnswerDiv = { style: { display: "block" } };

        // Mock getElementById to return the mock elements
        document.getElementById = jest.fn((id) => {
            if (id === "question_options") return mockQuestionOptions;
            if (id === "answer") return mockAnswerDiv;
        });
    });

    it("should populate the DOM with dropdown options", () => {
        const data = {
            question: {
                dropdown_options: ["Option 1", "Option 2", "Option 3"],
            },
        };

        // Call dropdown_display with mock data
        dropdown_display(data);

        // Check if the options are correctly added to the innerHTML of question_options
        expect(mockQuestionOptions.innerHTML).toContain('<select');
        expect(mockQuestionOptions.innerHTML).toContain('<option value="Option 1"></option>');
        expect(mockQuestionOptions.innerHTML).toContain('<option value="Option 2"></option>');
        expect(mockQuestionOptions.innerHTML).toContain('<option value="Option 3"></option>');
    });

    it("should set the answer display style to 'none'", () => {
        const data = {
            question: {
                dropdown_options: ["Option 1", "Option 2"],
            },
        };

        // Call dropdown_display with mock data
        dropdown_display(data);

        // Ensure that the answer div is hidden
        expect(mockAnswerDiv.style.display).toBe("none");
    });
});
