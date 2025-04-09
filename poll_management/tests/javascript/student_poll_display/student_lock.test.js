import { createLockOverlay } from "../../../static/js/student_poll_display/student_lock.js";

describe("createLockOverlay", () => {
    beforeEach(() => {
        // Clear the DOM before each test
        document.body.innerHTML = "";
    });

    it("should create and append the lock overlay if it does not exist", () => {
        createLockOverlay();

        const overlay = document.getElementById("poll-lock-overlay");
        expect(overlay).not.toBeNull();
        expect(overlay.className).toBe("poll-lock-overlay");
        expect(overlay.innerHTML).toContain("This question is locked");
        expect(overlay.innerHTML).toContain("Close");
    });

    it("should not create a duplicate overlay if one already exists", () => {
        // First call creates the overlay
        createLockOverlay();
        const firstOverlay = document.getElementById("poll-lock-overlay");

        // Second call should not create another overlay
        createLockOverlay();
        const overlays = document.querySelectorAll("#poll-lock-overlay");

        expect(overlays.length).toBe(1);
        expect(overlays[0]).toBe(firstOverlay);
    });

    it("should append styles to the document head", () => {
        createLockOverlay();

        const styleTags = document.querySelectorAll("style");
        expect(styleTags.length).toBeGreaterThan(0);
        expect(styleTags[0].textContent).toContain(".poll-lock-overlay");
    });

    it("should hide the overlay when 'Close' button is clicked", () => {
        createLockOverlay();
        const overlay = document.getElementById("poll-lock-overlay");
        overlay.style.display = "flex"; // Simulate it being visible

        const closeButton = document.getElementById("close-overlay-btn");
        closeButton.click();

        expect(overlay.style.display).toBe("none");
    });
});
