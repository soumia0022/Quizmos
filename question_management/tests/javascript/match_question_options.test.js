/**
 * @jest-environment jsdom
 */

const questionButtons = require('../../static/js/question_buttons');
const addMatchOptionComponents = questionButtons.addMatchOptionComponents;

describe('addMatchOptionComponents.js', () => {
    let matchQuestionOptionSection;
    let addMatchOptionButton;

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="match-question-options-container"></div>
            <button id="add-match-option">Add Option</button>
        `;

        matchQuestionOptionSection = document.getElementById('match-question-options-container');
        addMatchOptionButton = document.getElementById('add-match-option');
    });

    beforeAll(() => {
        // Mocking prompt if needed (optional)
        global.prompt = jest.fn(() => 'Mocked Option');
    });

    test('should add a match option when button is clicked', () => {
        let matchOptionCount = 1;

        // Event listener for button click
        addMatchOptionButton.addEventListener('click', () => {
            matchOptionCount = addMatchOptionComponents(matchQuestionOptionSection, matchOptionCount);
        });

        addMatchOptionButton.click();

        expect(matchOptionCount).toBe(2); // Match option count should increment
        expect(matchQuestionOptionSection.children.length).toBe(1); // One new option added
    });

    test('should create the correct elements when adding a match option', () => {
        let matchOptionCount = 1;

        // Trigger adding a match option
        matchOptionCount = addMatchOptionComponents(matchQuestionOptionSection, matchOptionCount);

        expect(matchOptionCount).toBe(2);
        expect(matchQuestionOptionSection.children.length).toBe(1);

        // Get the newly created option container
        const inputRow = matchQuestionOptionSection.children[0];

        // Check if the row is a div (container)
        expect(inputRow.tagName).toBe('DIV');
        expect(inputRow.children.length).toBe(3); // Should contain 3 children: input for option, input for answer, and delete button

        // Check for input for option
        const optionInput = inputRow.querySelector('input[type="text"][name="match_question_options[]"]');
        expect(optionInput).not.toBeNull();
        expect(optionInput.placeholder).toBe('Option 1');
        expect(optionInput.required).toBe(true);

        // Check for input for answer
        const answerInput = inputRow.querySelector('input[type="text"][name="match_question_answers[]"]');
        expect(answerInput).not.toBeNull();
        expect(answerInput.placeholder).toBe('Answer 1');
        expect(answerInput.required).toBe(true);

        // Check for delete button
        const deleteButton = inputRow.querySelector('button');
        expect(deleteButton).not.toBeNull();
        expect(deleteButton.textContent).toBe('X');
        expect(deleteButton.classList.contains('btn')).toBe(true);
        expect(deleteButton.classList.contains('btn-danger')).toBe(true);
        expect(deleteButton.classList.contains('btn-sm')).toBe(true);
    });

    test('should remove a match option when the delete button is clicked', () => {
        let matchOptionCount = 1;

        // Add a match option
        matchOptionCount = addMatchOptionComponents(matchQuestionOptionSection, matchOptionCount);

        const inputRow = matchQuestionOptionSection.children[0];

        expect(matchQuestionOptionSection.children.length).toBe(1);

        // Find the delete button and click it
        const deleteButton = inputRow.querySelector('button');
        deleteButton.click();

        expect(matchQuestionOptionSection.children.length).toBe(0); // Option should be removed
    });

});
