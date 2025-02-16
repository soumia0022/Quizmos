// questionTemplate.js
export function renderMultipleChoice(question) {
    return `<p>${question.text}</p>
            <div class="options-container" data-question="${question.id}">
              ${question.options.map((option, index) => `
                <div class="card response-card" style="margin-bottom: 10px; padding: 5px;">
                  <label>${option}</label>
                  <div class="response-stats">
                    <div class="progress-bar" style="width: 0%"></div>
                    <span class="response-percentage" data-option="${index}">0%</span>
                    <span class="response-count" data-option="${index}">0</span>
                  </div>
                </div>
              `).join('')}
            </div>`;
}

// Add the styles
const styles = `
    .response-card {
        position: relative;
        overflow: hidden;
    }
    
    .response-stats {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 5px;
    }
    
    .progress-bar {
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        background-color: rgba(0, 123, 255, 0.1);
        transition: width 0.3s ease;
        z-index: 0;
    }
    
    .response-percentage, .response-count {
        position: relative;
        z-index: 1;
        font-size: 0.9em;
        color: #666;
    }
`;

const styleSheet = document.createElement("style");
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);