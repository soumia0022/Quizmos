/**
 * @jest-environment jsdom
 */

const questionConstraints = require('../../static/js/question_constraints');
const {
    displayErrorMessage,
    McConstraints,
    ScConstraints,
    choiceQuestionConstraints
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

test('McConstraints should enforce constraints correctly', () => {
    const spy = jest.spyOn(questionConstraints, 'displayErrorMessage').mockImplementation(() => {});
    // Call McConstraints with valid options and answers
    McConstraints(['option1'], ['answer1'], 'multiple-choice');

    // Ensure displayErrorMessage was NOT called since valid input was provided
    expect(spy).not.toHaveBeenCalled();
    spy.mockRestore(); // Restore original function after test
});

test('McConstraints should show an error when no options are provided', () => {
    // Mock the alert function to check if it's called
    const alertMock = jest.spyOn(global, 'alert').mockImplementation(() => {});

    McConstraints([], ['answer1'], 'multiple-choice'); // No options

    // Ensure the alert was triggered with the expected message
    expect(alertMock).toHaveBeenCalledWith('Please add at least one option for the multiple-choice question.');

    alertMock.mockRestore(); // Clean up after the test
});

test('McConstraints should show an error when no answers are provided', () => {
    // Mock the alert function to check if it's called
    const alertMock = jest.spyOn(global, 'alert').mockImplementation(() => {});

    McConstraints(['option1'], [], 'multiple-choice'); // No answers

    expect(alertMock).toHaveBeenCalledWith('Please add at least one right answer for the multiple-choice question.');

    alertMock.mockRestore();
});

describe('ScConstraints', () => {
    beforeEach(() => {
        global.alert = jest.fn(); // Mock alert
    });

    test('should NOT show an error when a single answer is selected', () => {
        ScConstraints(['option1'], ['answer1'], 'single-choice');

        // Ensure no alert message is displayed
        expect(global.alert).not.toHaveBeenCalled();
    });

    test('should show an error message when multiple answers are selected for single-choice', () => {

        ScConstraints(['option1', 'option2'], ['answer1', 'answer2'], 'single-choice');

        // Ensure the correct alert message is displayed
        expect(global.alert).toHaveBeenCalledWith('You can only choose one right answer for single-choice question.');

    });

    test('should show an error message when no answers are selected for single-choice', () => {

        ScConstraints(['option1', 'option2'], [], 'single-choice');

        // Ensure the correct alert message is displayed
        expect(global.alert).toHaveBeenCalledWith('Please add at least one right answer for the single-choice question.');

    });

    test('should show an error message when no options are selected for single-choice', () => {

        ScConstraints([], ['answer1'], 'single-choice');

        // Ensure the correct alert message is displayed
        expect(global.alert).toHaveBeenCalledWith('Please add at least one option for the single-choice question.');

    });
});