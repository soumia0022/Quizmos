

document.addEventListener('DOMContentLoaded', function() {

    const importPdfBtn = document.getElementById('import-pdf-btn');
    const importDocBtn = document.getElementById('import-doc-btn');
    const pdfFileInput = document.getElementById('pdf-file-input');
    const docFileInput = document.getElementById('doc-file-input');


    importPdfBtn.addEventListener('click', function () {
        pdfFileInput.click();
    });

    importDocBtn.addEventListener('click', function () {
        docFileInput.click();
    });


    pdfFileInput.addEventListener('change', function (e) {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0], 'pdf');
        }
    });

    docFileInput.addEventListener('change', function (e) {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0], 'doc');
        }
    });

    function handleFileUpload(file, type) {
        const aiQuestionsArea = document.getElementById('ai-questions-area');
        aiQuestionsArea.innerHTML = `Processing ${type.toUpperCase()} file: ${file.name}...`;

        const formData = new FormData();
        formData.append('file', file);

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
                    aiQuestionsArea.innerHTML = `Error: ${data.error}`;
                } else if (data.questions) {
                    displayGeneratedQuestions(data.questions);
                }
            });
    }

    function displayGeneratedQuestions(questions) {
        const aiQuestionsArea = document.getElementById('ai-questions-area');

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


        const statusMessage = document.createElement('div');
        statusMessage.className = 'mt-3 p-2 text-center';
        statusMessage.style.backgroundColor = 'rgba(76, 175, 80, 0.2)';
        statusMessage.style.border = '1px solid #4CAF50';
        statusMessage.style.borderRadius = '4px';
        statusMessage.style.color = '#FFD700';
        statusMessage.innerHTML = `<p style="margin: 0;">Questions generated successfully! </p>`;
        aiQuestionsArea.appendChild(statusMessage);


        saveGeneratedQuestions(questions);
    }

    function saveGeneratedQuestions(questions) {

        console.log("Saving questions:", questions);
        console.log("Poll ID:", pollId);

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log("CSRF Token exists:", !!csrfToken);


        const saveUrl = '/save-generated-questions/';
        console.log("Save URL:", saveUrl);


        const payload = {
            poll_id: pollId,
            questions: questions
        };
        console.log("Request payload:", payload);


        fetch(saveUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            console.log("Response status:", response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);
            if (data.success) {
                const aiQuestionsArea = document.getElementById('ai-questions-area');
                const successMessage = document.createElement('div');
                successMessage.className = 'mt-3 p-2 text-center';
                successMessage.style.backgroundColor = 'rgba(76, 175, 80, 0.2)';
                successMessage.style.border = '1px solid #4CAF50';
                successMessage.style.borderRadius = '4px';
                successMessage.style.color = '#FFD700';
                successMessage.innerHTML = `<p style="margin: 0;">Questions successfully added to your poll! Page will refresh shortly...</p>`;

                const existingStatus = aiQuestionsArea.querySelector('.mt-3.p-2.text-center');
                if (existingStatus) {
                    existingStatus.replaceWith(successMessage);
                } else {
                    aiQuestionsArea.appendChild(successMessage);
                }

                setTimeout(() => location.reload(), 2000);
            }
        });
    }
});
