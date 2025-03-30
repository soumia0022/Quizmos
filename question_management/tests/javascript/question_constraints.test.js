/**
 * @jest-environment jsdom
 */

const {
    displayErrorMessage,
    canAddMoreOptions,
    McConstraints,
    ScConstraints,
    choiceQuestionConstraints,
    validateYouTubeLink
} = require('../../static/js/question_constraints');

describe('displayErrorMessage', () => {
    beforeEach(() => {
        global.alert = jest.fn(); // Mock alert function
    });

    test('should call alert and prevent event default', () => {
        const mockEvent = { preventDefault: jest.fn() };

        displayErrorMessage('Test message', mockEvent);

        expect(global.alert).toHaveBeenCalledWith('Test message');
        expect(mockEvent.preventDefault).toHaveBeenCalled();
    });
});

describe('canAddMoreOptions', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="multiple-choice-options-container">
                <div class="option"></div>
                <div class="option"></div>
            </div>
        `;
    });

    test('should return true if options are less than max limit', () => {
        expect(canAddMoreOptions('multiple-choice', 4)).toBe(true);
    });

    test('should return false if options reach the max limit', () => {
        document.getElementById('multiple-choice-options-container').innerHTML += `
            <div class="option"></div>
            <div class="option"></div>
        `;
        expect(canAddMoreOptions('multiple-choice', 4)).toBe(false);
    });

    test('should return true if container does not exist', () => {
        expect(canAddMoreOptions('non-existing-container', 4)).toBe(true);
    });
});

describe('McConstraints', () => {
    let choiceQuestionConstraintsMock;

    beforeEach(() => {
        choiceQuestionConstraintsMock = jest.spyOn(global, 'choiceQuestionConstraints').mockImplementation(() => {});
    });

    afterEach(() => {
        choiceQuestionConstraintsMock.mockRestore();
    });

    test('should call choiceQuestionConstraints', () => {
        McConstraints(['option1'], ['answer1'], 'multiple-choice');
        expect(choiceQuestionConstraintsMock).toHaveBeenCalledWith(['option1'], ['answer1'], 'multiple-choice');
    });
});

describe('ScConstraints', () => {
    beforeEach(() => {
        global.alert = jest.fn(); // Mock alert
    });

    test('should call choiceQuestionConstraints', () => {
        const choiceQuestionConstraintsMock = jest.spyOn(global, 'choiceQuestionConstraints').mockImplementation(() => {});
        ScConstraints(['option1'], ['answer1'], 'single-choice');
        expect(choiceQuestionConstraintsMock).toHaveBeenCalledWith(['option1'], ['answer1'], 'single-choice');
        choiceQuestionConstraintsMock.mockRestore();
    });

    test('should show error message when multiple answers are selected for single-choice', () => {
        const mockEvent = { preventDefault: jest.fn() };

        ScConstraints(['option1', 'option2'], ['answer1', 'answer2'], 'single-choice', mockEvent);

        expect(global.alert).toHaveBeenCalledWith('You can only choose one right answer for single-choice question.');
    });
});

describe('choiceQuestionConstraints', () => {
    beforeEach(() => {
        global.alert = jest.fn(); // Mock alert
    });

    test('should show error when no options are provided', () => {
        const mockEvent = { preventDefault: jest.fn() };

        choiceQuestionConstraints([], ['answer1'], 'multiple-choice', mockEvent);

        expect(global.alert).toHaveBeenCalledWith('Please add at least one option for the multiple-choice question.');
    });

    test('should show error when no answers are provided', () => {
        const mockEvent = { preventDefault: jest.fn() };

        choiceQuestionConstraints(['option1'], [], 'multiple-choice', mockEvent);

        expect(global.alert).toHaveBeenCalledWith('Please add at least one right answer for the multiple-choice question.');
    });

    test('should not show error when valid options and answers are provided', () => {
        const mockEvent = { preventDefault: jest.fn() };

        choiceQuestionConstraints(['option1'], ['answer1'], 'multiple-choice', mockEvent);

        expect(global.alert).not.toHaveBeenCalled();
    });
});
