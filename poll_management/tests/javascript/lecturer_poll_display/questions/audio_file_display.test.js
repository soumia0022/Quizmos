import { audio_file_display } from "../../../../static/js/lecturer_poll_display/questions/audio_file_display";

describe("audio_file_display", () => {
  it("should return the correct audio HTML with a valid audio file", () => {
    const question = { audio_file: "https://example.com/sample-audio.mp3" };

    const result = audio_file_display(question);

    expect(result).toContain('<div class="audio-container mb-3">');
    expect(result).toContain('<audio');
    expect(result).toContain('<source src="https://example.com/sample-audio.mp3" type="audio/mpeg">');
    expect(result).toContain("Your browser does not support the audio element.");
  });

  it("should not insert an undefined audio source when question.audio_file is missing", () => {
    const question = {
      audio_file: '',
    }; // No audio_file provided
    const result = audio_file_display(question);

    expect(result).toContain('<div class="audio-container mb-3">');
    expect(result).not.toContain('<source src="undefined"');
  });
});
