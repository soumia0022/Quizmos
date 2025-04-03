import { startCountdownTimer, getFormattedTime } from "../../static/js/timer.js";

// Mock window.unlock function
global.unlock = jest.fn();

describe("getFormattedTime", () => {
    it("should correctly format time in mm:ss", () => {
        expect(getFormattedTime(0)).toBe("00:00");
        expect(getFormattedTime(5)).toBe("00:05");
        expect(getFormattedTime(60)).toBe("01:00");
        expect(getFormattedTime(125)).toBe("02:05");
    });
});

describe("startCountdownTimer", () => {
    let questionElement, timerElement;

    beforeEach(() => {
        // Set up mock DOM
        document.body.innerHTML = `
            <div class="question">
                <span class="question-timer"></span>
            </div>
        `;
        questionElement = document.querySelector(".question");
        timerElement = questionElement.querySelector(".question-timer");

        jest.useFakeTimers(); // Mock setInterval
    });

    afterEach(() => {
        jest.useRealTimers();
    });

// it("should start the countdown and update the timer text", () => {
//     // Use fake timers to control setInterval and setTimeout
//     jest.useFakeTimers();
//
//     const timerInterval = startCountdownTimer(questionElement, 10);
//
//     // Check that the initial time is displayed correctly
//     expect(timerElement.textContent).toBe("Time remaining: 00:10");
//
//     // Simulate 3 seconds passing
//     jest.advanceTimersByTime(3000);
//
//     // Check that the timer updates after 3 seconds
//     expect(timerElement.textContent).toBe("Time remaining: 00:07");
//
//     // Clear the interval after test completion
//     clearInterval(timerInterval);
//
//     // Restore real timers after test
//     jest.useRealTimers();
// });


    it("should stop and display 'Time's up!' when time reaches zero", () => {
        const timerInterval = startCountdownTimer(questionElement, 5);

        jest.advanceTimersByTime(5000); // Simulate 5 seconds
        expect(timerElement.textContent).toBe("Time's up!");

        // Ensure `window.unlock()` was called when timer expired
        expect(global.unlock).toHaveBeenCalled();

        clearInterval(timerInterval);
    });
});
