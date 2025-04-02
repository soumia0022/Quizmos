/**
 * @jest-environment jsdom
 */

import "../../static/js/lecturer_poll_display/poll"; // Ensure script runs
import { renderChoice } from "../../static/js/lecturer_poll_display/questions/choice_display";
import { pollState } from "../../static/js/lecturer_poll_display/../poll_state";

jest.mock("../../static/js/lecturer_poll_display/questions/choice_display", () => ({
  renderChoice: jest.fn(() => "<div>Mocked Choice</div>"),
}));

jest.mock("../../static/js/lecturer_poll_display/../poll_state", () => ({
  pollState: {
    lecturer_webSocket: { readyState: 1, send: jest.fn() }, // Mock WebSocket
    currentQuestion: null,
  },
}));

describe("startPoll", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <button id="start-poll-btn" style="display: block;"></button>
      <div id="question-display" style="display: none;"></div>
      <button id="unlock" style="display: none;"></button>
      <button id="show-answer-closed" style="display: none;"></button>
      <button id="show-answer-open" style="display: inline;"></button>
      <div id="question-container"></div>
      <button id="prev-btn"></button>
      <button id="next-btn"></button>
    `;

    // Define global state for testing
    window.questions = [{ id: 1, type: "multiple_choice", text: "Question 1" }];
    window.currentQuestionIndex = 0;

    pollState.currentQuestion = window.questions[0];
  });

  it("should update the DOM correctly when startPoll is called", () => {
    window.startPoll();

    expect(document.getElementById("start-poll-btn").style.display).toBe("none");
    expect(document.getElementById("question-display").style.display).toBe("block");
    expect(document.getElementById("unlock").style.display).toBe("");
    expect(document.getElementById("show-answer-closed").style.display).toBe("inline");
    expect(document.getElementById("show-answer-open").style.display).toBe("none");
  });
});

import { updateQuestionDisplay } from "../../static/js/lecturer_poll_display/poll";

describe("updateQuestionDisplay", () => {
  it("should render the correct question HTML", () => {
    updateQuestionDisplay(); // Call it directly instead of using `window.updateQuestionDisplay`

    expect(renderChoice).toHaveBeenCalledWith(window.questions[0]);
    expect(document.getElementById("question-container").innerHTML).toContain("Mocked Choice");
  });

  it("should disable prev button on first question", () => {
    updateQuestionDisplay();

    expect(document.getElementById("prev-btn").disabled).toBe(true);
  });
});

