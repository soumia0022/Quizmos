// questions.js
export class QuestionManager {
    constructor(questions, webSocket) {
        this.questions = questions;
        this.currentIndex = 0;
        this.webSocket = webSocket;
    }

    getCurrentQuestion() {
        return this.questions[this.currentIndex];
    }

    shuffleArray(array) {
        return [...array].sort(() => Math.random() - 0.5);
    }

    DropdownFillHTML(question) {
        const parts = question.text.split('___');
        let html = '<div class="question-title"><p>';

        parts.forEach((part, index) => {
            html += part;
            if (index < parts.length - 1) {
                html += '&nbsp;&nbsp;&nbsp;';
            }
        });

        html += '</p><div class="options-container">';
        html += question.options.map(option =>
            `<div class="card option-card" data-option="${option}">
                <div class="card-body">${option}</div>
             </div>`
        ).join('');
        html += '</div></div>';

        return html;
    }

    TextFillHTML(question) {
        return `
            <div class="question-title">
                <p>${question.text}</p>
                <div class="form-group">
                    <div class="form-control mt-3" style="height: auto; min-height: 50px; border: 1px solid #ced4da; padding: 10px;">
                    Type your answer here
                  </div>
                </div>
            </div>`;
    }

    ChoiceHTML(question) {
        return `
            <div class="question-title">
                <p>${question.text}</p>
                <div class="options-container">
                    ${question.options.map((option, index) => `
                        <div class="card option-card mb-2">
                            <div class="card-body">
                                <div class="form-check">
                                    <label for="option${index}">${option}</label>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>`;
    }

    WordcloudHTML(question) {
        return `
            <div class="question-title">
                <p>${question.text}</p>
                
                <div class="form-control wordcloud-input mt-3" 
                  <div class=" mt-3" style="height: auto; min-height: 50px; border: 1px solid #ced4da; padding: 10px; background-color: #f8f9fa;">
                    Word cloud will appear here
                  </div>
                </div>
            </div>`;
    }

    MatchQuestionHTML(question) {
        const shuffledAnswers = this.shuffleArray(question.answers);
        return `
            <div class="question-title">
                <p>${question.text}</p>
                <div class="matching-container mt-3">
                    ${question.options.map((option, index) => `
                        <div class="matching-item mb-3">
                            <div class="row">
                                <div class="col-5">
                                    <div class="card p-3 text-center option-card" 
                                         data-option-index="${index}">
                                        <span class="option-text">${option}</span>
                                    </div>
                                </div>
                                <div class="col-5">
                                    <div class="card p-3 text-center answer-card" 
                                         data-answer-index="${index}">
                                        <span class="answer-text">${shuffledAnswers[index]}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>`;
    }

    createQuestionHTML(question) {
        switch(question.type) {
            case 'dropdown_fill':
                return this.DropdownFillHTML(question);
            case 'text_fill':
                return this.TextFillHTML(question);
            case 'multiple_choice':
                return this.ChoiceHTML(question);
            case 'single_choice':
                return this.ChoiceHTML(question);
            case 'wordcloud':
                return this.WordcloudHTML(question);
            case 'match_question':
                return this.MatchQuestionHTML(question);
            default:
                return '<p>Unsupported question type</p>';
        }
    }

    updateDisplay() {
        const questionContainer = document.getElementById('question-container');
        const currentQuestion = this.getCurrentQuestion();

        questionContainer.innerHTML = this.createQuestionHTML(currentQuestion);

        // Update navigation buttons
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        prevBtn.disabled = this.currentIndex === 0;
        nextBtn.disabled = this.currentIndex === this.questions.length - 1;

        // Notify WebSocket about question change
        if (this.webSocket && this.webSocket.readyState === WebSocket.OPEN) {
            this.webSocket.send(JSON.stringify({
                type: 'question',
                question_id: currentQuestion.id
            }));
        }
        
    }
    

    next() {
        if (this.currentIndex < this.questions.length - 1) {
            this.currentIndex++;
            this.updateDisplay();
            return true;
        }
        return false;
    }

    previous() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updateDisplay();
            return true;
        }
        return false;
    }
}