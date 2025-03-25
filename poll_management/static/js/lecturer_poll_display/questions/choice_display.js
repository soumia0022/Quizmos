

export function renderChoice(question) {
    return `
            <p>${question.text}</p>
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
