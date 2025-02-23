/**
 * @jest-environment jsdom
 */

const questionButtons = require('../../static/js/question_buttons');
const addSingleChoiceOption = questionButtons.addSingleChoiceOption;

describe('single_choice_options.js', () => {
    let singleChoiceOptionsSection;
    let scButton;

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="single-choice-options-container"></div>
            <button id="add-sc-option">Add Option</button>
        `;

        singleChoiceOptionsSection = document.getElementById('single-choice-options-container');
        scButton = document.getElementById('add-sc-option');
    });

    beforeAll(() => {
        global.prompt = jest.fn(() => 'Mocked Option');
    });

    test('should add a single-choice option when button is clicked', () => {
        let count = 1;
        scButton.addEventListener('click', () => {
            count = addSingleChoiceOption(count, singleChoiceOptionsSection);
        });

        scButton.click();

        expect(count).toBe(2);
        expect(singleChoiceOptionsSection.children.length).toBe(1);
    });

    test('should fail to add an option with no text', () => {
        const promptMock = jest.spyOn(global, 'prompt').mockReturnValue(null);

        let count = 1;
        scButton.addEventListener('click', () => {
            count = addSingleChoiceOption(count, singleChoiceOptionsSection);
        });

        scButton.click();

        expect(count).toBe(1);
        expect(singleChoiceOptionsSection.children.length).toBe(0);

        promptMock.mockRestore();
    });

    test('should create the correct elements when adding a single-choice option', () => {
        jest.spyOn(global, 'prompt').mockReturnValue('Mocked Option');

        let count = 1;
        count = addSingleChoiceOption(count, singleChoiceOptionsSection);

        expect(count).toBe(2);
        expect(singleChoiceOptionsSection.children.length).toBe(1);

        const optionContainer = singleChoiceOptionsSection.children[0];

        expect(optionContainer.tagName).toBe('DIV');
        expect(optionContainer.classList.contains('single_choice-option')).toBe(true);

        const hiddenInput = optionContainer.querySelector('input[type="hidden"]');
        expect(hiddenInput).not.toBeNull();
        expect(hiddenInput.name).toBe('single_choice_options[]');
        expect(hiddenInput.value).toBe('Mocked Option');

        const checkbox = optionContainer.querySelector('input[type="checkbox"]');
        expect(checkbox).not.toBeNull();
        expect(checkbox.name).toBe('single_choice_answers[]');
        expect(checkbox.value).toBe('Mocked Option');

        const label = optionContainer.querySelector('label');
        expect(label).not.toBeNull();
        expect(label.textContent).toBe('Mocked Option');

        const deleteButton = optionContainer.querySelector('button.delete-option-btn');
        expect(deleteButton).not.toBeNull();
        expect(deleteButton.textContent).toBe('X');

        global.prompt.mockRestore();
    });
});
