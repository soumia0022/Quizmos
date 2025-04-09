import {pollState} from "../../../../static/js/poll_state";
import { choice_display } from '../../../../static/js/student_poll_display/questions/choice_display.js';

describe('choice_display', () => {
    let mockQuestionOptions, mockAnswerDiv;

    beforeEach(() => {
        jest.clearAllMocks();
        // Mock DOM elements
        mockQuestionOptions = {
            innerHTML: "",
            appendChild: jest.fn(function (child) {
                this.innerHTML += child.outerHTML; // Simulating real appendChild
            }),
        };
        mockAnswerDiv = { style: { display: "block" } };

        document.getElementById = jest.fn((id) => {
            if (id === 'question_options') return mockQuestionOptions;
            if (id === 'answer') return mockAnswerDiv;
        });
        console.log('pollState:', pollState);
    });

    it('should generate radio buttons for single-choice questions', () => {
        const data = { question: { single_option: ["Option A", "Option B"] } };
        pollState.selectedAnswers = null;

        choice_display(data, "single");

        expect(mockQuestionOptions.innerHTML).toBe(
            `<div class="question-section">` +
                `<div class="option-item" data-value="Option A"><label></label></div>` +
                `<div class="option-item" data-value="Option B"><label></label></div>` +
            `</div>`
        );

        expect(mockAnswerDiv.style.display).toBe("none");
    });


    it('should generate checkboxes for multiple-choice questions', () => {
        const data = { question: { mcq_options: ["Option 1", "Option 2", "Option 3"] } };

        choice_display(data, "multiple");

        expect(mockQuestionOptions.innerHTML).toBe(
            `<div class="question-section">` +
                `<div class="option-item" data-value="Option 1"><label></label></div>` +
                `<div class="option-item" data-value="Option 2"><label></label></div>` +
                `<div class="option-item" data-value="Option 3"><label></label></div>` +
            `</div>`
        );

        expect(mockAnswerDiv.style.display).toBe("none");
    });


    it('should handle an empty options array', () => {
        const data = { question: { single_option: [] } };

        choice_display(data, "single");

        expect(mockQuestionOptions.innerHTML).toBe("<div class=\"question-section\"></div>"); // Should render nothing
        expect(mockAnswerDiv.style.display).toBe("none");
    });
});
