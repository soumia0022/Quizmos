import {renderCodeQuestion} from "../../../../static/js/lecturer_poll_display/questions/code_question_display";

describe('renderCodeQuestion', () => {
  it('should render HTML structure with question data', () => {
    // Mock question object
    const question = {
      id: '123',
      text: 'What is your favorite programming language?',
    };

    // Call the function
    const result = renderCodeQuestion(question);

    // Check if the result includes the correct HTML structure and question data
    expect(result).toContain('<div class="question-container" data-question="123">');
    expect(result).toContain('<p>What is your favorite programming language?</p>');
    expect(result).toContain('id="responseList-123"');
  });
});