/**
 * @jest-environment jsdom
 */

import { WordCloudGenerator } from "../../../../static/js/lecturer_poll_display/questions/word_cloud_generator.js";

// Mock getBBox globally to prevent Jest errors
SVGElement.prototype.getBBox = function () {
  return { width: 100, height: 20 };
};

// Debugging: Log the class
console.log(WordCloudGenerator);  // Should log the class or `undefined` if it's not exported correctly

describe("WordCloudGenerator", () => {
  let container;

  beforeEach(() => {
    document.body.innerHTML = `<div id="word-cloud-container"></div>`;
    container = document.getElementById("word-cloud-container");
  });

  it("should create an SVG element inside the container", () => {
    // Initialize the WordCloudGenerator
    const wordCloud = new WordCloudGenerator('word-cloud-container');
    wordCloud.generate({ test: 1 }); // Pass some mock data

    // Assert that an SVG element was created inside the container
    expect(container.querySelector("svg")).not.toBeNull();
  });

  it("should filter out words containing '****'", () => {
    const wcg = new WordCloudGenerator("word-cloud-container");
    const wordData = {
      "hello": 5,
      "bad****": 3,
      "world": 2
    };

    wcg.generate(wordData);

    const texts = Array.from(container.querySelectorAll("text")).map(el => el.textContent);
    expect(texts).toContain("hello");
    expect(texts).toContain("world");
    expect(texts).not.toContain("bad****");
  });

  it("should display 'No words submitted yet' when no words are provided", () => {
    const wcg = new WordCloudGenerator("word-cloud-container");
    wcg.generate({});
    expect(container.textContent).toContain("No words submitted yet");
  });

  it("should display 'No appropriate words to display' when all words are filtered out", () => {
    const wcg = new WordCloudGenerator("word-cloud-container");
    const wordData = {
      "****bad": 10,
      "****hidden": 8
    };

    wcg.generate(wordData);
    expect(container.textContent).toContain("No appropriate words to display");
  });

  it("should correctly place words inside the SVG", () => {
    const wcg = new WordCloudGenerator("word-cloud-container", { width: 300, height: 200 });

    const wordData = { "test": 10 };
    wcg.generate(wordData);

    const wordElement = container.querySelector("text");
    expect(wordElement).not.toBeNull();
    expect(parseInt(wordElement.getAttribute("x"))).toBeGreaterThan(0);
    expect(parseInt(wordElement.getAttribute("y"))).toBeGreaterThan(0);
  });

  it("should create words with different font sizes based on frequency", () => {
    const wcg = new WordCloudGenerator("word-cloud-container", { minFontSize: 10, maxFontSize: 50 });

    const wordData = { "small": 1, "big": 10 };
    wcg.generate(wordData);

    const words = Array.from(container.querySelectorAll("text"));
    const sizes = words.map(el => parseFloat(el.getAttribute("font-size")));

    expect(Math.max(...sizes)).toBeGreaterThan(Math.min(...sizes));
  });
});
