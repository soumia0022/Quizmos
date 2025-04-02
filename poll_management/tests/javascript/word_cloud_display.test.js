import {renderWordCloud} from "../../static/js/lecturer_poll_display/questions/word_cloud_display";

describe("renderWordCloud", () => {
  it("should generate the correct HTML for a given question", () => {
    // Mock question object
    const question = { id: 123, text: "What are your thoughts?" };

    // Call the function
    const result = renderWordCloud(question);

    // Expected structure
    expect(result).toContain('<p>What are your thoughts?</p>');
    expect(result).toContain('<div id="word-cloud-123" class="word-cloud-container"></div>');
  });

  it("should handle an empty question text", () => {
    const question = { id: 456, text: "" };

    const result = renderWordCloud(question);

    expect(result).toContain('<p></p>');
    expect(result).toContain('<div id="word-cloud-456" class="word-cloud-container"></div>');
  });
});
