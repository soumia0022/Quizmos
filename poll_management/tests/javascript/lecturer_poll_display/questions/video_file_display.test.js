import { video_file_display } from "../../../../static/js/lecturer_poll_display/questions/video_file_display";

describe('video_file_display', () => {
  it('should return the correct video HTML', () => {
    const question = {
      video_file: 'https://youtu.be/Zfb2z82Aw_Q',
    };

    const html = video_file_display(question);

    expect(html).toContain('<div class="video-container mb-3">');
    expect(html).toContain('<source src="https://youtu.be/Zfb2z82Aw_Q" type="video/mp4">');
    expect(html).toContain('Your browser does not support the video element.');
  });

  it('should not insert an undefined video source when question.video_file is missing', () => {
    const question = {
      video_file: '',
    };

    const html = video_file_display(question);

    expect(html).toContain('<div class="video-container mb-3">');
    expect(html).not.toContain('<source src="undefined"');
  });
});
