import {pollState} from "../../../static/js/poll_state";
import {showAnswer} from "../../../static/js/lecturer_poll_display/show_answer"

describe('showAnswer', () => {
    let mockClosedEyeButton;
    let mockOpenEyeButton;

    beforeEach(() => {
        // Mock the document.getElementById function
        mockClosedEyeButton = { style: { display: "" } };
        mockOpenEyeButton = { style: { display: "none" } };

        document.getElementById = jest.fn((id) => {
            if (id === 'show-answer-closed') return mockClosedEyeButton;
            if (id === 'show-answer-open') return mockOpenEyeButton;
        });

        // Mock the window objects
        window.questions = [{ id: 1 }];
        window.currentQuestionIndex = 0;

        // Mock the pollState
        pollState.lecturer_webSocket = {
            send: jest.fn(),
        };
    });

    it('should show the answer when the closed eye button is visible', () => {
        // Set the closed eye button to be visible
        mockClosedEyeButton.style.display = "inline";

        // Call the showAnswer function
        showAnswer();

        // Check that the display styles were updated
        expect(mockClosedEyeButton.style.display).toBe("none");
        expect(mockOpenEyeButton.style.display).toBe("inline");

        // Check that the send method was called with the correct data
        expect(pollState.lecturer_webSocket.send).toHaveBeenCalledWith(
            JSON.stringify({
                type: 'show_answers',
                question_id: 1,
                action: 'show_answer'
            })
        );
    });

    it('should not do anything if window.questions or window.currentQuestionIndex is undefined', () => {
        // Set the window variables to undefined
        window.questions = undefined;
        window.currentQuestionIndex = undefined;

        // Mock the send function (it should not be called)
        pollState.lecturer_webSocket.send.mockClear();

        // Call the showAnswer function
        showAnswer();

        // Check that the send method was not called
        expect(pollState.lecturer_webSocket.send).not.toHaveBeenCalled();
    });

    it('should not do anything if questionId is undefined', () => {
        // Set the questionId to undefined
        window.questions[window.currentQuestionIndex].id = undefined;

        // Mock the send function (it should not be called)
        pollState.lecturer_webSocket.send.mockClear();

        // Call the showAnswer function
        showAnswer();

        // Check that the send method was not called
        expect(pollState.lecturer_webSocket.send).not.toHaveBeenCalled();
    });
});
