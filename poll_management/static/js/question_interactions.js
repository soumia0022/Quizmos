function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }
  
  function initializeSortable() {
    const rightContainer = document.getElementById('right');
  
    if (rightContainer) {
      new Sortable(rightContainer, {
        group: "shared",
        animation: 150
      });
    }
  
    const dropzones = document.querySelectorAll('.dropzone');
    dropzones.forEach(dropzone => {
      if (dropzone) {
        new Sortable(dropzone, {
          group: "shared",
          animation: 150,
          onAdd: function(evt) {
            if (dropzone.children.length > 1) {
              const oldItem = dropzone.children[0];
              rightContainer.appendChild(oldItem);
            }
          }
        });
      }
    });
  }
  
  function renderMatchQuestion(data) {
    let leftOptions = "";
    let rightOptions = "";
  
    data.question.match_options.forEach((option) => {
      leftOptions += `
        <div class="flex-container">
          <div class="box left">${option}</div>
          <div class="dropzone-box dropzone right"></div>
        </div>`;
    });
  
    const shuffledAnswers = shuffleArray([...data.question.match_answers]);
  
    shuffledAnswers.forEach(answer => {
      rightOptions += `<div class="box draggable" draggable="true">${answer}</div>`;
    });
  
    document.getElementById('question_options').innerHTML = `
      <div id="options-container" class="flex-container">
        <div id="left" class="left">${leftOptions}</div>
      </div>
      <div class="row">
        <div id="right" class="right">${rightOptions}</div>
      </div>`;
  
    initializeSortable();
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    const questionTypeElement = document.getElementById('question_type');
    const questionType = questionTypeElement ? questionTypeElement.value : null;
  
    if (questionType === 'match_question') {
      const pollCodeElement = document.getElementById('poll_code');
      const pollCode = pollCodeElement ? pollCodeElement.value : null;
  
      if (pollCode) {
        // Live mode with WebSocket
        const ws = new WebSocket(`ws://${window.location.host}/ws/poll/${pollCode}/`);
  
        ws.onmessage = function(event) {
          const data = JSON.parse(event.data);
  
          if (data.type === 'question' && data.question.type === 'match_question') {
            renderMatchQuestion(data);
          }
        };
      } else {
        // Preview mode without WebSocket
        // The question data is embedded in the HTML as JSON script
        const questionDataElement = document.getElementById('question_data');
        if (questionDataElement) {
          const data = JSON.parse(questionDataElement.textContent);
          renderMatchQuestion(data);
        }
      }
    }
  });
  