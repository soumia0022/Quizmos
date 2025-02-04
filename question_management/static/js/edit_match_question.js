document.addEventListener('DOMContentLoaded', function () {
    const questionType = document.getElementById("question-type").value

    const matchQuestionOptionSection = document.getElementById('match-options-container');
    const matchQuestionSetSection = document.getElementById('match-pre-filled-options')
    const matchQuestionAddBtn = document.getElementById('match-add-option-btn');

    // Ensure sections exist before counting their children
    //Check to make sure the first 2 ones are working properly
    let matchOptionCount = matchQuestionSetSection ? (matchQuestionSetSection.children.length) : 1;

    const deleteButtons = document.querySelectorAll('.delete-option-btn');

    deleteButtons.forEach((btn) => {
        btn.addEventListener('click', function () {
            const optionContainer = this.parentElement; // Get the div containing the option
            console.log(optionContainer.id)
            optionContainer.remove(); // Remove the option
        });
    });

    if (matchQuestionAddBtn){
        matchQuestionAddBtn.addEventListener("click", () => {
            const inputRow = document.createElement("div");

            const option = document.createElement("input");
            option.type = "text";
            option.placeholder = `Option ${matchOptionCount}`;
            option.name = 'match_question_options[]';
            option.required = true;

            const answer = document.createElement("input");
            answer.type = "text";
            answer.placeholder = `Answer ${matchOptionCount}`;
            answer.name = 'match_question_answers[]';
            answer.required = true;

            // Create delete button
            const deleteBtn = document.createElement('button');
            deleteBtn.type = 'button';
            deleteBtn.className = 'btn btn-danger btn-sm ms-2';
            deleteBtn.textContent = 'X';
            deleteBtn.addEventListener('click', function () {
                inputRow.remove(); // Remove the option container
                matchOptionCount--;
            });

            inputRow.appendChild(option);
            inputRow.appendChild(answer)
            inputRow.appendChild(deleteBtn)

            matchQuestionOptionSection.appendChild(inputRow);
            matchOptionCount++;
        });
    }

    // TO DO: Ensure question text is filled before submission
     document.querySelector('form').addEventListener('submit', function (event) {
         console.log("question type is: ", questionType)
         if (questionType === 'match_question'){
            const options = document.querySelectorAll('[name="match_question_options[]"]')
            if (options.length === 0) {
                alert('Please add at least one matching card option for the match question.');
                event.preventDefault(); //don't allow the submission to go thru
            }
        }
    });
});