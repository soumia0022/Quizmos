// Define `html` globally before importing the function
global.html = '';

import { video_file_display } from "../../../../static/js/lecturer_poll_display/questions/video_file_display";

describe('video_file_display', () => {

  beforeEach(() => {
    global.html = ''; // Reset it before each test
  });

  it('should append the correct video HTML to the existing html variable', () => {
    const question = {
      video_file: 'https://youtu.be/Zfb2z82Aw_Q',
    };

    video_file_display(question);

    expect(global.html).toContain('<div class="video-container mb-3">');
    expect(global.html).toContain('<source src="https://youtu.be/Zfb2z82Aw_Q" type="video/mp4">');
    expect(global.html).toContain('Your browser does not support the video element.');
  });

  it('should not insert an undefined video source when question.video_file is missing', () => {
    const question = {
      video_file: '',
    }; // No video_file provided

    video_file_display(question);

    expect(global.html).toContain('<div class="video-container mb-3">');
    expect(global.html).not.toContain('<source src="undefined"');
  });
});
