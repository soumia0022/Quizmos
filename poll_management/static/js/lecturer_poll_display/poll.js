import {fetchResponseCounts} from './websocket.js';
import {renderChoice} from "./questions/choice_display.js";
import {renderText} from "./questions/text_question_display.js";
import {renderWordCloud} from "./questions/word_cloud_display.js";
import {renderMatch} from "./questions/match_question_display.js";
import {getFormattedTime, startCountdownTimer} from "../timer.js";
import { renderCodeQuestion } from "./questions/code_question_display.js";
import {pollState} from "../poll_state.js";
import {video_file_display} from "./questions/video_file_display.js";
import {audio_file_display} from "./questions/audio_file_display.js";
import {youtube_video_display} from "./questions/youtube_video_display.js";


window.startPoll = function() {
    document.getElementById('start-poll-btn').style.display = 'none';
    document.getElementById('question-display').style.display = 'block';
    document.getElementById('unlock').style.display = '';
    document.getElementById('show-answer-closed').style.display = 'inline';
    document.getElementById('show-answer-open').style.display = 'none';
    updateQuestionDisplay();
};

window.previousQuestion = function() {
    if (window.currentQuestionIndex > 0) {
        window.currentQuestionIndex--;
        updateQuestionDisplay();
        resetShowAnswerState();
        lock();
        fetchResponseCounts(window.questions[window.currentQuestionIndex].id);
    }
};

window.nextQuestion = function() {
    if (window.currentQuestionIndex < window.questions.length - 1) {
        window.currentQuestionIndex++;
        updateQuestionDisplay();
        resetShowAnswerState();
        lock();
        fetchResponseCounts(window.questions[window.currentQuestionIndex].id);
    }
};

function resetShowAnswerState() {
    const closedEyeButton = document.getElementById('show-answer-closed');
    const openEyeButton = document.getElementById('show-answer-open');
    document.getElementById('correct-answers').style.display = 'none';;
    const currentQuestion = window.questions[window.currentQuestionIndex];

  // hide eye icon for wordcloud questions
  if (currentQuestion.type === 'wordcloud') {
    closedEyeButton.style.display = 'none';
    openEyeButton.style.display = 'none';
  } else {
    closedEyeButton.style.display = 'inline';
    openEyeButton.style.display = 'none';

    const questionId = currentQuestion.id;
    if (pollState.lecturer_webSocket.readyState === WebSocket.OPEN) {
        pollState.lecturer_webSocket.send(JSON.stringify({
            type: 'show_answers',
            question_id: questionId,
            action: 'hide_answer'
        }));
    }
  }
  }

function createQuestionHTML(question) {
  let html = '<div class="question-title">';//this will store the final html content needed to display the question


  if (question.youtube_link != null) {
    const embedURL = question.youtube_link.replace("youtu.be/", "www.youtube.com/embed/");
    html += youtube_video_display(embedURL);
    }

  if (question.video_file != null) {
    html += video_file_display(question);
  }

  if (question.audio_file != null) {
    html += audio_file_display(question);
    }

  if (question.question_timer != null) {
      // get the formatted time
      const formattedTime = `${getFormattedTime(question.question_timer)}`;
      html += `<div class="question-timer">Time remaining: ${formattedTime}</div>`;
    }

  switch(question.type) {
    case 'dropdown_fill':
    case 'multiple_choice':
    case 'single_choice':
        html += renderChoice(question);
        break;

    case 'text_fill':
        html += renderText(question);
        break;

    case 'wordcloud':
      html += renderWordCloud(question);
      break;

    case 'match_question':
       html += renderMatch(question);
       break;

   case 'code_question':
       html += renderCodeQuestion(question);


break;
  }

  html += '</div>';
  return html;
}

function updateQuestionDisplay() {
    const questionContainer = document.getElementById('question-container');
    const currentQuestion = pollState.currentQuestion= window.questions[window.currentQuestionIndex];
    pollState.currentQuestionId=currentQuestion.id;
    pollState.currentQuestionType= currentQuestion.type;
    pollState.code_language = currentQuestion.code_language;

    // Update the question display (only set innerHTML once)
    questionContainer.innerHTML = createQuestionHTML(currentQuestion);

  // Hide eye icons for word cloud questions
  const closedEyeButton = document.getElementById('show-answer-closed');
  const openEyeButton = document.getElementById('show-answer-open');
  if (currentQuestion.type === 'wordcloud') {
      closedEyeButton.style.display = 'none';
      openEyeButton.style.display = 'none';
  } else {
    
      closedEyeButton.style.display = 'inline'; 
      openEyeButton.style.display = 'none';
  }

    if (window.currentTimerInterval) {
        clearInterval(window.currentTimerInterval);
        window.currentTimerInterval = null;
    }
    if (currentQuestion.question_timer != null) {
        window.currentTimerInterval = startCountdownTimer(questionContainer, currentQuestion.question_timer);
    }

    // Update navigation buttons
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    prevBtn.disabled = window.currentQuestionIndex === 0;
    nextBtn.disabled = window.currentQuestionIndex === window.questions.length - 1;

    // Send question update to WebSocket
    if (pollState.lecturer_webSocket.readyState === WebSocket.OPEN) {
      pollState.lecturer_webSocket.send(JSON.stringify({
        type: 'question',
        question_id: currentQuestion.id,
        question_timer: currentQuestion.question_timer,
      }));
    }
  }

export {updateQuestionDisplay};