import { showFeedback } from "../../../static/js/student_poll_display/show_feedback.js";

describe("showFeedback", () => {
    let mockFeedback;

    beforeEach(() => {
        // Mock the feedback element
        mockFeedback = {
            textContent: "",
            className: "",
            style: { display: "none" },
        };

        // Mock document.getElementById to return the feedback element
        document.getElementById = jest.fn(() => mockFeedback);

        // Mock setTimeout to execute immediately
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.clearAllTimers();
    });

    it("should display success feedback", () => {
        showFeedback("Success message", true);

        expect(mockFeedback.textContent).toBe("Success message");
        expect(mockFeedback.className).toBe("feedback success");
        expect(mockFeedback.style.display).toBe("block");

        // Simulate the timeout
        jest.advanceTimersByTime(3000);
        expect(mockFeedback.style.display).toBe("none");
    });

    it("should display error feedback", () => {
        showFeedback("Error message", false);

        expect(mockFeedback.textContent).toBe("Error message");
        expect(mockFeedback.className).toBe("feedback error");
        expect(mockFeedback.style.display).toBe("block");

        // Simulate the timeout
        jest.advanceTimersByTime(3000);
        expect(mockFeedback.style.display).toBe("none");
    });
});
