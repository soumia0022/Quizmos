import {renderText} from "../../../../static/js/lecturer_poll_display/questions/text_question_display";

describe('renderText', () => {
  it('should render HTML with the correct question data', () => {
    // Mock question object with id and text
    const question = {
      id: '1',
      text: 'What is your favorite color?',
    };

    // Call the renderText function
    const result = renderText(question);

    // Check if the result includes the correct HTML structure and question data
    expect(result).toContain('<div class="question-container" data-question="1">');
    expect(result).toContain('<p>What is your favorite color?</p>');
    expect(result).toContain('Type your answer here');
  });

  it('should handle empty question text', () => {
    // Mock question object with empty text
    const question = {
      id: '2',
      text: '',
    };

    // Call the renderText function
    const result = renderText(question);

    // Check if it still renders the HTML structure, even with empty text
    expect(result).toContain('<div class="question-container" data-question="2">');
    expect(result).toContain('<p></p>');  // Empty question text
    expect(result).toContain('Type your answer here');
  });

  it('should render the correct response list container with the given question id', () => {
    // Mock question object with id
    const question = {
      id: '3',
      text: 'What is your name?',
    };

    // Call the renderText function
    const result = renderText(question);

    // Check if the response list container has the correct id attribute
    expect(result).toContain('<ul id="responseList-3" class="list-group response-list">');
  });
});
