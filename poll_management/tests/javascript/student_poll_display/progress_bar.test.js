import { updateProgressBar } from "../../../static/js/student_poll_display/progress_bar.js";

describe("updateProgressBar", () => {
    let mockProgressBar, mockProgressText;

    beforeEach(() => {
        // Mock progress bar and progress text elements
        mockProgressBar = {
            style: { width: "" },
            setAttribute: jest.fn(),
            classList: {
                add: jest.fn(),
                remove: jest.fn(),
            },
        };

        mockProgressText = { textContent: "" };

        // Mock document.getElementById
        document.getElementById = jest.fn((id) => {
            if (id === "question-progress-bar") return mockProgressBar;
            if (id === "question-progress-text") return mockProgressText;
        });
    });

    it("should update progress bar width and aria-valuenow correctly", () => {
        updateProgressBar(3, 10); // 30% progress

        expect(mockProgressBar.style.width).toBe("30%");
        expect(mockProgressBar.setAttribute).toHaveBeenCalledWith("aria-valuenow", 30);
    });

    it("should update progress text correctly", () => {
        updateProgressBar(5, 10);

        expect(mockProgressText.textContent).toBe("Question 5 of 10");
    });

    it("should apply 'bg-danger' class for 25% or lower progress", () => {
        updateProgressBar(2, 10); // 20% progress

        expect(mockProgressBar.classList.remove).toHaveBeenCalledWith("bg-warning", "bg-success");
        expect(mockProgressBar.classList.add).toHaveBeenCalledWith("bg-danger");
    });

    it("should apply 'bg-warning' class for progress between 25% and 75%", () => {
        updateProgressBar(4, 10); // 40% progress

        expect(mockProgressBar.classList.remove).toHaveBeenCalledWith( "bg-danger", "bg-success");
        expect(mockProgressBar.classList.add).toHaveBeenCalledWith("bg-warning");
    });

    it("should apply 'bg-success' class for 75% or higher progress", () => {
        updateProgressBar(8, 10); // 80% progress

        expect(mockProgressBar.classList.remove).toHaveBeenCalledWith("bg-danger", "bg-warning");
        expect(mockProgressBar.classList.add).toHaveBeenCalledWith("bg-success");
    });

    it("should handle total = 0 gracefully (prevent division by zero)", () => {
        updateProgressBar(1, 0);

        expect(mockProgressBar.style.width).toBe("0%");
        expect(mockProgressBar.setAttribute).toHaveBeenCalledWith("aria-valuenow", 0);
        expect(mockProgressText.textContent).toBe("Question 1 of 0");
    });

    it("should do nothing if progress bar or text elements are missing", () => {
        document.getElementById = jest.fn(() => null);

        expect(() => updateProgressBar(5, 10)).not.toThrow();
    });
});
