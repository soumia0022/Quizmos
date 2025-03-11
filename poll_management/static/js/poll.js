import {fetchResponseCounts, ws} from './websocket.js';
import {renderChoice} from "./choice_display.js";
import {renderText} from "./text_question_display.js";
import {renderWordCloud} from "./word_cloud_display.js";
import {renderMatch} from "./match_question_display.js";
import {getFormattedTime, startCountdownTimer} from "./timer.js";
import { renderCodeQuestion } from "./code_question_display.js";



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
        fetchResponseCounts(window.questions[window.currentQuestionIndex].id);
    }
};

window.nextQuestion = function() {
    if (window.currentQuestionIndex < window.questions.length - 1) {
        window.currentQuestionIndex++;
        updateQuestionDisplay();
        resetShowAnswerState();
        fetchResponseCounts(window.questions[window.currentQuestionIndex].id);
    }
};

function resetShowAnswerState() {
    const closedEyeButton = document.getElementById('show-answer-closed');
    const openEyeButton = document.getElementById('show-answer-open');
    closedEyeButton.style.display = 'inline';
    openEyeButton.style.display = 'none';

    // notify the server to hide answers and show the closed eye icon 
    const questionId = window.questions[window.currentQuestionIndex].id;
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'show_answers',
            question_id: questionId,
            action: 'hide_answer'
        }));
    }
}

function createQuestionHTML(question) {
  let html = '<div class="question-title">';//this will store the final html content needed to display the question


  if (question.youtube_link != null) {
    const embedURL = question.youtube_link.replace("youtu.be/", "www.youtube.com/embed/");
    html += `
       <div class="video-container">
        <iframe 
            width="560" 
            height="315" 
            src="${embedURL}" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
    </div>
    `;
    }

  if (question.video_file != null) {
    html += `
      <div class="video-container mb-3">
        <video 
          controls
          width="100%" 
          style="max-width: 640px;"
          class="rounded"
        >
          <source src="${question.video_file}" type="video/mp4">
          Your browser does not support the video element.
        </video>
      </div>
    `;
  }

  if (question.audio_file != null) {
  html += `
    <div class="audio-container mb-3">
      <audio 
        controls
        class="w-100"
        style="max-width: 640px;"
      >
        <source src="${question.audio_file}" type="audio/mpeg">
        Your browser does not support the audio element.
      </audio>
    </div>
    `;
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
    const currentQuestion = window.questions[window.currentQuestionIndex];

    // Update the question display (only set innerHTML once)
    questionContainer.innerHTML = createQuestionHTML(currentQuestion);


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
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'question',
        question_id: currentQuestion.id,
        question_timer: currentQuestion.question_timer,
      }));
    }
}