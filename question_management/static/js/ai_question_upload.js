

document.addEventListener('DOMContentLoaded', function() {

    const textInput = document.getElementById('text-input');
    const charCounter = document.getElementById('char-counter');
    const generateQuestionsBtn = document.getElementById('generate-questions-btn');
    const aiQuestionsArea = document.getElementById('ai-questions-area');


    textInput.addEventListener('input', function() {

        const text = this.value;


        const currentLength = text.length;
        charCounter.textContent = `${currentLength}/1000 characters`;


        if (currentLength > 900 && currentLength <= 950) {
            charCounter.style.color = '#ff9900';
        } else if (currentLength > 950) {
            charCounter.style.color = '#ff6b6b';
        } else {
            charCounter.style.color = '#FFD700';
        }
    });


    generateQuestionsBtn.addEventListener('click', function() {
        const text = textInput.value.trim();


        if (!text) {
            aiQuestionsArea.innerHTML = `
                <span style="color: #ff6b6b; display: block; text-align: center; margin-top: 50px;">
                    Please enter some text to generate questions.
                </span>
            `;
            return;
        }

        if (text.length > 1000) {
            aiQuestionsArea.innerHTML = `
                <span style="color: #ff6b6b; display: block; text-align: center; margin-top: 50px;">
                    Text exceeds 1000 characters. Please shorten your input.
                </span>
            `;
            return;
        }


        aiQuestionsArea.innerHTML = `
            <span style="color: #FFD700; display: block; text-align: center; margin-top: 50px;">
                Processing text: ${text.length} characters...
                <br><br>
                This may take a moment
            </span>
        `;


        const formData = new FormData();
        formData.append('text', text);


        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;


        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                aiQuestionsArea.innerHTML = `
                    <span style="color: #ff6b6b; display: block; text-align: center; margin-top: 50px;">
                        Error: ${data.error}
                    </span>
                `;
            } else if (data.questions) {
                displayGeneratedQuestions(data.questions);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            aiQuestionsArea.innerHTML = `
                <span style="color: #ff6b6b; display: block; text-align: center; margin-top: 50px;">
                    An error occurred while generating questions. Please try again.
                </span>
            `;
        });
    });


    function displayGeneratedQuestions(questions) {
        aiQuestionsArea.innerHTML = questions.map((q, index) =>
            `<div class="generated-question">
                <h4>Question ${index + 1}</h4>
                <p><strong>${q.question}</strong></p>
                <ul>
                    ${q.options.map(opt => 
                        `<li class="${opt === q.answer ? 'correct-answer' : ''}">${opt}</li>`
                    ).join('')}
                </ul>
                <p><strong>Correct Answer:</strong> ${q.answer}</p>
                <hr>
            </div>`
        ).join('');
    }
});