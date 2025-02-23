/**
 * @jest-environment jsdom
 */

const questionButtons = require('../../static/js/question_buttons');
const addMultipleChoiceOption = questionButtons.addMultipleChoiceOption;
const addSingleChoiceOption = questionButtons.addSingleChoiceOption;

describe('add_question.js', () => {
    let multipleChoiceOptionsSection;
    let singleChoiceOptionsSection;

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="multiple-choice-options-container"></div>
            <div id="single-choice-options-container"></div>
        `;

        multipleChoiceOptionsSection = document.getElementById('multiple-choice-options-container');
        singleChoiceOptionsSection = document.getElementById('single-choice-options-container');
    });

    // jest can't wait for user input for the prompts so it uses a fixed string to simulate the prompts
    beforeAll(() => {
        global.prompt = jest.fn(() => 'Mocked Option'); // Always return a fixed string
    });

    test('should add a multiple-choice option', () => {
        let count = 1;
        count = addMultipleChoiceOption(count, multipleChoiceOptionsSection);

        expect(count).toBe(2); // Count should increment
        expect(multipleChoiceOptionsSection.children.length).toBe(1); // Option added
    });

    test('should add a single-choice option', () => {
        let count = 1;
        count = addSingleChoiceOption(count, singleChoiceOptionsSection);

        expect(count).toBe(2);
        expect(singleChoiceOptionsSection.children.length).toBe(1);
    });

    test('should fail to add an option with no text', () => {
        // Mock prompt just for this test to return null (no input or cancellation)
        const promptMock = jest.spyOn(global, 'prompt').mockReturnValue(null);

        let count = 1;
        count = addMultipleChoiceOption(count, multipleChoiceOptionsSection);

        expect(count).toBe(1); // Count shouldn't increment
        expect(multipleChoiceOptionsSection.children.length).toBe(0); // Option shouldn't be added

        // Clean up the mock after the test - turns it back to the global prompt in before all
        promptMock.mockRestore();
    });
});
