export function renderMatch(question) {
    return ` 
 <div class="match-question" data-question="${question.id}">
   <p>${question.text}</p>
   <div class="matching-container mt-3">
     ${question.options.map(option => {
       // Replace spaces with underscores or remove them completely
       const safeOption = option.replace(/\s+/g, '_');
       return `
       <div class="matching-item mb-4">
         <h6 class="mb-3">Option "${option}":</h6>
         <div class="match-responses">
           ${question.answers.map(answer => {
             // Replace spaces with underscores or remove them in answers too
             const safeAnswer = answer.replace(/\s+/g, '_');
             return `
             <div class="match-response-row mb-2" id="match-${safeOption}-${safeAnswer}">
               <div class="d-flex justify-content-between align-items-center">
                 <span class="answer-text">${answer}</span>
                 <div class="response-stats">
                   <div class="d-flex align-items-center gap-2">
                     <span class="response-percentage">0%</span>
                     <span class="response-count text-muted">(0)</span>
                     <div class="progress" style="width: 100px; height: 8px;">
                       <div class="progress-bar" role="progressbar" 
                            style="width: 0%" 
                            aria-valuenow="0" 
                            aria-valuemin="0" 
                            aria-valuemax="100">
                       </div>
                     </div>
                   </div>
                 </div>
               </div>
             </div>
           `}).join('')}
         </div>
       </div>
     `}).join('')}
   </div>
 </div>
`;
     }