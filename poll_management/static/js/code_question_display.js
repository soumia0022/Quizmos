export function renderCodeQuestion(question) {
    return `
            <div class="question-container" data-question="${question.id}">
            <p>${question.text}</p>
              <div class="form-group">
                <div class="form-control mt-3" style="height: auto; min-height: 50px; border: 1px solid #ced4da; padding: 10px; background-color: #f8f9fa;">
                  Run your code in the IDE
                </div>
              </div>
              <div class="response-list-container mt-3">
                <h6>Responses:</h6>
                <ul id="responseList-${question.id}" class="list-group response-list">
                  <!-- Responses will be inserted here -->
                </ul>
              </div>
            </div>`;
}
