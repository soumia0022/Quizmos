import { match_display } from "../../../../static/js/student_poll_display/questions/match_display.js";

// Define initializeDragAndDrop globally
global.initializeDragAndDrop = jest.fn();

// Mock shuffleArray to return a fixed order
jest.spyOn(global.Math, "random").mockReturnValue(0.5);

describe("match_display", () => {
    let mockQuestionOptions, mockAnswerDiv;

    beforeEach(() => {
        // Mock DOM elements
        mockQuestionOptions = { innerHTML: "" };
        mockAnswerDiv = { style: { display: "block" } };

        document.getElementById = jest.fn((id) => {
            if (id === "question_options") return mockQuestionOptions;
            if (id === "answer") return mockAnswerDiv;
        });

        // Reset mock call counts before each test
        global.initializeDragAndDrop.mockClear();
    });

    it("should populate the DOM with matching question options and answers", () => {
        const data = {
            question: {
                match_options: ["Option A", "Option B"],
                match_answers: ["Answer 1", "Answer 2"],
            },
        };

        match_display(data);

        expect(mockQuestionOptions.innerHTML).toContain(`<div class=\"match-box left\">Option A</div>`);
        expect(mockQuestionOptions.innerHTML).toContain(`<div class=\"match-box left\">Option B</div>`);
        expect(mockQuestionOptions.innerHTML).toContain(`<div class="box draggable">Answer 1</div>`);
        expect(mockQuestionOptions.innerHTML).toContain(`<div class="box draggable">Answer 2</div>`);

        expect(mockAnswerDiv.style.display).toBe("none");
    });

    it("should call initializeDragAndDrop", () => {
        const data = {
            question: {
                match_options: ["Option A", "Option B"],
                match_answers: ["Answer 1", "Answer 2"],
            },
        };

        match_display(data);

        // Expect initializeDragAndDrop to have been called
        expect(global.initializeDragAndDrop).toHaveBeenCalled();
    });

    it("should handle empty match options and answers", () => {
        const data = {
            question: {
                match_options: [],
                match_answers: [],
            },
        };

        match_display(data);

        expect(mockQuestionOptions.innerHTML).toContain(`<div class="match-container">`);
        expect(mockQuestionOptions.innerHTML.replace(/\s+/g, '')).toContain('<divid="right"class="right"></div>');
        expect(mockAnswerDiv.style.display).toBe("none");
    });
});
