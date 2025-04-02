/**
 * @jest-environment jsdom
 */

import { youtube_video_display } from "../../static/js/lecturer_poll_display/questions/youtube_video_display.js";

describe("youtube_video_display", () => {
  it("should return a valid HTML string containing an iframe", () => {
    const embedURL = "https://www.youtube.com/embed/example";
    const result = youtube_video_display(embedURL);

    // Create a temporary container to parse the HTML string
    const container = document.createElement("div");
    container.innerHTML = result;

    // Select the iframe element
    const iframe = container.querySelector("iframe");

    // Assertions
    expect(iframe).not.toBeNull(); // Ensures iframe is present
    expect(iframe.getAttribute("src")).toBe(embedURL); // Ensures correct embed URL
    expect(iframe.getAttribute("width")).toBe("560"); // Ensures width is set
    expect(iframe.getAttribute("height")).toBe("315"); // Ensures height is set
    expect(iframe.hasAttribute("allowfullscreen")).toBe(true); // Ensures allowfullscreen is present
  });
});
