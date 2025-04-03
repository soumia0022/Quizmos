import { choice_display } from '../../../../static/js/student_poll_display/questions/choice_display.js';

describe('choice_display', () => {
    let mockQuestionOptions, mockAnswerDiv;

    beforeEach(() => {
        // Mock DOM elements
        mockQuestionOptions = { innerHTML: "" };
        mockAnswerDiv = { style: { display: "block" } };

        document.getElementById = jest.fn((id) => {
            if (id === 'question_options') return mockQuestionOptions;
            if (id === 'answer') return mockAnswerDiv;
        });
    });

    it('should generate radio buttons for single-choice questions', () => {
        const data = { question: { single_option: ["Option A", "Option B"] } };

        choice_display(data, "single");

        expect(mockQuestionOptions.innerHTML).toBe(
            `<div><input type="radio" name= "single_choice" value="Option A"><label>Option A</label></div>` +
            `<div><input type="radio" name= "single_choice" value="Option B"><label>Option B</label></div>`
        );

        expect(mockAnswerDiv.style.display).toBe("none");
    });

    it('should generate checkboxes for multiple-choice questions', () => {
        const data = { question: { mcq_options: ["Option 1", "Option 2", "Option 3"] } };

        choice_display(data, "multiple");

        expect(mockQuestionOptions.innerHTML).toBe(
            `<div><input type="checkbox" name= "multiple_choice" value="Option 1"><label>Option 1</label></div>` +
            `<div><input type="checkbox" name= "multiple_choice" value="Option 2"><label>Option 2</label></div>` +
            `<div><input type="checkbox" name= "multiple_choice" value="Option 3"><label>Option 3</label></div>`
        );

        expect(mockAnswerDiv.style.display).toBe("none");
    });

    it('should handle an empty options array', () => {
        const data = { question: { single_option: [] } };

        choice_display(data, "single");

        expect(mockQuestionOptions.innerHTML).toBe(""); // Should render nothing
        expect(mockAnswerDiv.style.display).toBe("none");
    });
});
