import {renderMatch} from "../../../../static/js/lecturer_poll_display/questions/match_question_display";

describe('renderMatch', () => {
  it('should render HTML with question data and match options', () => {
    // Mock question object with options and answers
    const question = {
      id: '123',
      text: 'Match the programming languages to their creators:',
      options: ['Python', 'JavaScript', 'Ruby'],
      answers: ['Guido van Rossum', 'Brendan Eich', 'Yukihiro Matsumoto'],
    };

    // Call the function
    const result = renderMatch(question);

    // Check if the result includes the correct HTML structure and question data
    expect(result).toContain('<div class="match-question" data-question="123">');
    expect(result).toContain('<p>Match the programming languages to their creators:</p>');
    expect(result).toContain('Option "Python":');
    expect(result).toContain('Guido van Rossum');
    expect(result).toContain('id="match-Python-Guido_van_Rossum"');
  });

  it('should replace spaces with underscores in option and answer ids', () => {
    // Mock question object with spaces in options and answers
    const question = {
      id: '456',
      text: 'Match the frameworks to their creators:',
      options: ['Angular JS', 'Vue JS'],
      answers: ['Google', 'Evan You'],
    };

    // Call the function
    const result = renderMatch(question);

    // Check if spaces are replaced with underscores in ids
    expect(result).toContain('id="match-Angular_JS-Google"');
    expect(result).toContain('id="match-Vue_JS-Evan_You"');
  });

  it('should render correctly with no options or answers', () => {
    // Mock question object with no options or answers
    const question = {
      id: '789',
      text: 'No options or answers here',
      options: [],
      answers: [],
    };

    // Call the function
    const result = renderMatch(question);

    // Ensure the result contains the question text but no options or answers
    expect(result).toContain('<p>No options or answers here</p>');
    expect(result).not.toContain('<div class="matching-item">');
  });
});
