/**
 * @jest-environment jsdom
 */

const questionButtons = require('../../static/js/question_buttons');
const addMultipleChoiceOption = questionButtons.addMultipleChoiceOption;

describe('multiple_choice_options.js', () => {
    let multipleChoiceOptionsSection;
    let mcButton;

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="multiple-choice-options-container"></div>
            <button id="add-mc-option">Add Option</button>
        `;

        multipleChoiceOptionsSection = document.getElementById('multiple-choice-options-container');
        mcButton = document.getElementById('add-mc-option');
    });

    beforeAll(() => {
        global.prompt = jest.fn(() => 'Mocked Option'); // Always return a fixed string
    });

    test('should add a multiple-choice option when button is clicked', () => {
        let count = 1;
        mcButton.addEventListener('click', () => {
            count = addMultipleChoiceOption(count, multipleChoiceOptionsSection);
        });

        mcButton.click();

        expect(count).toBe(2);
        expect(multipleChoiceOptionsSection.children.length).toBe(1);
    });

    test('should fail to add an option with no text', () => {
        const promptMock = jest.spyOn(global, 'prompt').mockReturnValue(null);

        let count = 1;
        mcButton.addEventListener('click', () => {
            count = addMultipleChoiceOption(count, multipleChoiceOptionsSection);
        });

        mcButton.click();

        expect(count).toBe(1);
        expect(multipleChoiceOptionsSection.children.length).toBe(0);

        promptMock.mockRestore();
    });

    test('should create the correct elements when adding a multiple-choice option', () => {
        jest.spyOn(global, 'prompt').mockReturnValue('Mocked Option');

        let count = 1;
        count = addMultipleChoiceOption(count, multipleChoiceOptionsSection);

        expect(count).toBe(2);
        expect(multipleChoiceOptionsSection.children.length).toBe(1);

        const optionContainer = multipleChoiceOptionsSection.children[0];

        expect(optionContainer.tagName).toBe('DIV');
        expect(optionContainer.classList.contains('multiple-choice-option')).toBe(true);

        const hiddenInput = optionContainer.querySelector('input[type="hidden"]');
        expect(hiddenInput).not.toBeNull();
        expect(hiddenInput.name).toBe('multiple_choice_options[]');
        expect(hiddenInput.value).toBe('Mocked Option');

        const checkbox = optionContainer.querySelector('input[type="checkbox"]');
        expect(checkbox).not.toBeNull();
        expect(checkbox.name).toBe('multiple_choice_answers[]');
        expect(checkbox.value).toBe('Mocked Option');

        const label = optionContainer.querySelector('label');
        expect(label).not.toBeNull();
        expect(label.textContent).toBe('Mocked Option');

        const deleteButton = optionContainer.querySelector('button.delete-option-btn');
        expect(deleteButton).not.toBeNull();
        expect(deleteButton.textContent).toBe('X');

        global.prompt.mockRestore();
    });

    test('should remove an option when the delete button is clicked', () => {
        jest.spyOn(global, 'prompt').mockReturnValue('Mocked Option');
        let count = 1;
        count = addMultipleChoiceOption(count, multipleChoiceOptionsSection);

        const optionContainer = multipleChoiceOptionsSection.children[0];

        expect(multipleChoiceOptionsSection.children.length).toBe(1);

        // Simulate clicking the delete button
        const deleteButton = optionContainer.querySelector('button.delete-option-btn');
        deleteButton.click();

        expect(multipleChoiceOptionsSection.children.length).toBe(0); // Option should be removed

        global.prompt.mockRestore();
    });
});
