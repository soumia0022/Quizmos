export function renderCodeQuestion(question) {
    console.log("code_question_display.js is loaded");
    return `
            <div class="question-container" data-question="${question.id}">
            <p>${question.text}</p>
              <div class="form-group">
                <div class="form-control mt-3" style="height: auto; min-height: 50px; border: 1px solid #ced4da; padding: 10px; background-color: #f8f9fa;">
                  Run your code in the IDE
                </div>
              </div>
            </div>`;
}
