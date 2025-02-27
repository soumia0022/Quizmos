export function renderWordCloud(question) {
    return `<p>${question.text}</p>
               <div class="form-group">
                <div class="form-control mt-3" style="height: auto; min-height: 50px; border: 1px solid #ced4da; padding: 10px; background-color: #f8f9fa;">
                  Type your answer here
                </div>
              </div>`;
}