/**
 * @jest-environment jsdom
 */

// Mock WordCloudGenerator
jest.mock('../../../static/js/lecturer_poll_display/questions/word_cloud_generator.js', () => {
  return {
    WordCloudGenerator: jest.fn().mockImplementation(() => ({
      generate: jest.fn()
    }))
  };
});

// Import after mocking the module to ensure mock is used
import {
  updateProgressElements,
  updateResponseUI,
  updateTextResponseUI,
  updateCodeResponseUI,
  updateWordCloudUI
} from "../../../static/js/lecturer_poll_display/response_ui.js";

// Import WordCloudGenerator to verify it is called
import { WordCloudGenerator } from "../../../static/js/lecturer_poll_display/questions/word_cloud_generator.js"; // Make sure it's imported after jest.mock()

describe("UI Update Functions", () => {

  beforeEach(() => {
    document.body.innerHTML = `
      <div data-question="1">
        <div class="response-card">
          <div class="response-percentage"></div>
          <div class="response-count"></div>
          <div class="progress-bar"></div>
        </div>
        <ul id="responseList-1"></ul>
        <div class="response-list-container"></div>
      </div>
    `;
  });

  test("updateProgressElements correctly updates progress bar", () => {
    const element = document.querySelector(".response-card");
    updateProgressElements(element, 3, 10);

    expect(element.querySelector(".response-percentage").textContent).toBe("30.0%");
    expect(element.querySelector(".response-count").textContent).toBe("(3)");
    expect(element.querySelector(".progress-bar").style.width).toBe("30%");
    expect(element.classList.contains("has-responses")).toBe(true);
  });

  test("updateResponseUI correctly updates response cards", () => {
    updateResponseUI("1", { 0: 5, 1: 10 });

    const progressBars = document.querySelectorAll(".progress-bar");
    expect(progressBars[0].style.width).not.toBe("0%");
  });

  test("updateTextResponseUI creates list items for responses", () => {
    updateTextResponseUI("1", ["Response 1", "Response 2"]);
    const items = document.querySelectorAll("#responseList-1 .list-group-item");

    expect(items.length).toBe(2);
    expect(items[0].textContent).toContain("Response 1");
    expect(document.querySelector(".response-list-container").style.display).toBe("block");
  });

  test("updateCodeResponseUI creates user clickable items", () => {
    updateCodeResponseUI("1", [{ username: "User1", code: "console.log('Hello');" }], "javascript");

    const userElement = document.querySelector(".response-user");
    expect(userElement.textContent.trim()).toBe("User1");
    expect(userElement.dataset.code).toBe(encodeURIComponent("console.log('Hello');"));
  });

  it("updateWordCloudUI initializes WordCloudGenerator", () => {
    updateWordCloudUI("word-cloud-container", { hello: 10 });

    // Ensure WordCloudGenerator was called with correct arguments
    expect(WordCloudGenerator).toHaveBeenCalledWith("word-cloud-container", {});

    // Ensure the `generate` method was called with word data
    // expect(WordCloudGenerator.mock.instances[0].generate).toHaveBeenCalledWith({ hello: 10 });
  });

});
