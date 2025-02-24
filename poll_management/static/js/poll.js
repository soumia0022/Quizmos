function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
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

  switch(question.type) {
     case 'dropdown_fill':
      const parts = question.text.split('___'); // split the text where there are blank spaces (3 underscores ___)
      html += `<p>`;
      parts.forEach((part, index) => {
        html += part; // for each part in the question, add it to the HTML content
        if (index < parts.length - 1) {
          // Add some empty spaces (3 spaces per blank)
          html += '&nbsp;&nbsp;&nbsp;';
        }
      });
       html += `</p>`;
       html += `<div class="options-container">
             ${question.options.map(option =>
               `<div class="card" style="margin-bottom: 10px; padding: 5px;">
                 <label>${option}</label>
               </div>`
             ).join('')}
           </div>`;
      break;

    case 'text_fill':
      html += `<p>${question.text}</p>
               <div class="form-group">
                <div class="form-control mt-3" style="height: auto; min-height: 50px; border: 1px solid #ced4da; padding: 10px; background-color: #f8f9fa;">
                  Type your answer here
                </div>
              </div>`

      break;

    case 'multiple_choice':
      html += `<p>${question.text}</p>
               <div class="options-container">
                 ${question.options.map(option => `
                   <div class="card" style = "margin-bottom: 10px; padding: 5px;">
                     <label >${option}</label>
                   </div>
                 `).join('')}
               </div>`;
      break;

    case 'single_choice':
      html += `<p>${question.text}</p>
               <div class="options-container">
                 ${question.options.map(option => `
                   <div class="card" style = "margin-bottom: 10px; padding: 5px;">
                     <label >${option}</label>
                   </div>
                 `).join('')}
               </div>`;
      break;

      case 'wordcloud':
        html += `<p>${question.text}</p>
          <div class="form-group">
            <input type="text" id="answer1" name="word_cloud_response1" class="form-control mt-3" placeholder="Your first answer" />
            <input type="text" id="answer2" name="word_cloud_response2" class="form-control mt-3" placeholder="Your second answer (optional)" />
          </div>`;
      break;

    case 'match_question':

      const shuffledAnswers = shuffleArray([...question.answers]);

       html += `<p>${question.text}</p>
         <div class="matching-container mt-3">
           ${question.options.map((option, index) => `
             <div class="matching-item mb-3">
               <div class="row">
                 <div class="col-5">
                   <div class="card p-3 text-center">
                     <span class="option-text">${option}</span>
                   </div>
                 </div>
                 <div class="col-5">
                   <div class="card p-3 text-center">
                     <span class="answer-text">${shuffledAnswers[index]}</span>
                   </div>
                 </div>
               </div>
             </div>
           `).join('')}
         </div>`;
break;
  }

  html += '</div>';
  return html;
}

  function updateQuestionDisplay() {
    const questionContainer = document.getElementById('question-container');
    const currentQuestion = questions[currentQuestionIndex];

    // Update the question display
    questionContainer.innerHTML = createQuestionHTML(currentQuestion);

    // Update navigation buttons
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.disabled = currentQuestionIndex === questions.length - 1;

    // Send question update to WebSocket
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'question',
        question_id: currentQuestion.id
      }));
    }
  }

  function previousQuestion() {
    if (currentQuestionIndex > 0) {
      currentQuestionIndex--;
      updateQuestionDisplay();
    }
  }

  function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
      currentQuestionIndex++;
      updateQuestionDisplay();
    }
  }

  function startPoll() {
    document.getElementById('start-poll-btn').style.display = 'none';
    document.getElementById('question-display').style.display = 'block';
    document.getElementById('unlock').style.display = '';

    updateQuestionDisplay();
  }

