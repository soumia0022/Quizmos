import { startCountdownTimer } from "../timer.js";
import {initializeCodeEditor, executeCode} from "../code_executor.js";

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

        function showFeedback(message, isSuccess) {
            const feedback = document.getElementById('feedback');
            feedback.textContent = message;
            feedback.className = `feedback ${isSuccess ? 'success' : 'error'}`;
            feedback.style.display = 'block';
            setTimeout(() => {
                feedback.style.display = 'none';
            }, 3000);
        }

        let currentQuestionId = null;
        let currentQuestionType = null;
        let currentTimerInterval = null;
        let currentQuestion = null;
        let answerCodeEditor = null;

        document.addEventListener('DOMContentLoaded', function() {
            const pollCodeElement = document.getElementById('poll-container');
            const pollCode = pollCodeElement ? pollCodeElement.dataset.pollCode : null;
            console.log(pollCode);
            const ws = new WebSocket(`ws://${window.location.host}/ws/poll/${pollCode}/`);
            const submitButton = document.getElementById('submitResponse');

            // Function to update the progress bar
            let totalQuestions = 0;
            let currentQuestionNumber = 0;

            function updateProgressBar(currentNum, total) {
                const progressBar = document.getElementById('question-progress-bar');
                const progressText = document.getElementById('question-progress-text');

                if (!progressBar || !progressText) return;

                const percentage = total > 0 ? (currentNum / total) * 100 : 0;

                progressBar.style.width = `${percentage}%`;
                progressBar.setAttribute('aria-valuenow', percentage);
                progressText.textContent = `Question ${currentNum} of ${total}`;

                // The color changes based on question progression
                if (percentage <= 25) {
                    progressBar.classList.remove('bg-warning', 'bg-success');
                    progressBar.classList.add('bg-danger');
                } else if (percentage > 25 && percentage < 75) {
                    progressBar.classList.remove('bg-danger', 'bg-success');
                    progressBar.classList.add('bg-warning');
                } else {
                    progressBar.classList.remove('bg-danger', 'bg-warning');
                    progressBar.classList.add('bg-success');
                }
            }

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                console.log(data);
                // Handle poll lock/unlock messages
                if (data.type === 'poll_status') {
                    if (data.action === 'lock') {
                        showLockOverlay();
                    } else if (data.action === 'unlock') {
                        hideLockOverlay();
                    }
                }
                // Handle answers display
                if (data.type === 'answers') {

                    const correctAnswersDiv = document.getElementById('correct-answers');

                    if (data.action === 'show_answer') {
                        let answerHtml = '<strong>Correct Answer(s):</strong> ';

                        switch (currentQuestionType) {
                            case 'multiple_choice':
                            case 'single_choice':
                                answerHtml += Array.isArray(data.answers) ? data.answers.join(', ') : data.answers;
                                break;
                            case 'dropdown_fill':
                            case 'text_fill':
                                answerHtml += data.answers;
                                break;
                            case 'match_question':
                                if (Array.isArray(data.answers) && currentQuestion && currentQuestion.match_options) {
                                    answerHtml += data.answers.map((ans, idx) =>
                                        `${currentQuestion.match_options[idx]} → ${ans}`).join(', ');
                                } else {
                                    answerHtml += 'Matching pairs are shown.';
                                }
                                break;
                            case 'wordcloud':
                                answerHtml += 'No correct answer for word cloud.';
                                break;
                            case 'code_question':
                                answerHtml = '<strong>Correct Answer:</strong><div id="answer-code-display"></div>';
                                correctAnswersDiv.innerHTML = answerHtml;

                                // Get the code language from the current question
                                let language = currentQuestion && currentQuestion.code_language ?
                                    currentQuestion.code_language : "python";

                                // Create a textarea for the code editor
                                const codeTextarea = document.createElement('textarea');
                                codeTextarea.id = 'answer-code-editor';
                                document.getElementById('answer-code-display').appendChild(codeTextarea);

                                // Initialize CodeMirror for the answer
                                answerCodeEditor = initializeCodeEditor(codeTextarea, language);

                                // Set the answer code and make it read-only
                                answerCodeEditor.setValue(data.answers);
                                answerCodeEditor.setOption('readOnly', true);
                                setTimeout(() => answerCodeEditor.refresh(), 100);
                                correctAnswersDiv.style.display = 'block';
                                return;
                        }

                        correctAnswersDiv.innerHTML = answerHtml;
                        correctAnswersDiv.style.display = 'block';
                    } else if (data.action === 'hide_answer') {
                        correctAnswersDiv.style.display = 'none';
                        correctAnswersDiv.innerHTML = '';

                        // Clean up CodeMirror instance if it exists
                        if (answerCodeEditor) {
                            answerCodeEditor = null;
                        }
                    }
                }

                if (data.type === 'question') {
                    // Clear any existing timer
                    if (currentTimerInterval) {
                        clearInterval(currentTimerInterval);
                    }

                    // Reset correct answers display
                    const correctAnswersDiv = document.getElementById('correct-answers');
                    correctAnswersDiv.style.display = 'none';
                    correctAnswersDiv.innerHTML = '';

                    // Clean up CodeMirror instance if it exists
                    if (answerCodeEditor) {
                        answerCodeEditor = null;
                    }

                    const questionElement = document.getElementById('question');
                    questionElement.innerHTML = data.question.text + '<div class="question-timer"></div>';

                    // start timer
                    if (data.question.question_timer) {
                        currentTimerInterval = startCountdownTimer(questionElement, data.question.question_timer);
                    }

                    currentQuestionId = data.question.id;
                    currentQuestionType = data.question.type;
                    currentQuestion = data.question;
                    submitButton.style.display = 'block';

                    // Update question progress information
                    if (data.total_questions) {
                        totalQuestions = data.total_questions;
                    }
                    if (data.question_number) {
                        currentQuestionNumber = data.question_number;
                    }

                    // Update the progress bar
                    updateProgressBar(currentQuestionNumber, totalQuestions);

                    if (data.question.type === 'multiple_choice') {
                        let options = "";
                        data.question.mcq_options.forEach(option => {
                            options += `<div><input type="checkbox" value="${option}"><label>${option}</label></div>`;
                        });
                        document.getElementById('question_options').innerHTML = options;
                        document.getElementById('answer').style.display = 'none';

                    } else if (data.question.type === 'single_choice') {
                        let options = "";
                        data.question.single_option.forEach(option => {
                            options += `<div><input type="radio" name="single_choice" value="${option}"><label>${option}</label></div>`;
                        });
                        document.getElementById('question_options').innerHTML = options;
                        document.getElementById('answer').style.display = 'none';

                    } else if (data.question.type === 'dropdown_fill') {
                        let options = '<select><option value="" disabled selected>Select an option</option>';
                        data.question.dropdown_options.forEach(option => {
                            options += `<option value="${option}">${option}</option>`;
                        });
                        options += '</select>';
                        document.getElementById('question_options').innerHTML = options;
                        document.getElementById('answer').style.display = 'none';

                    } else if (data.question.type === 'text_fill') {
                        document.getElementById('question_options').innerHTML = '';
                        document.getElementById('answer').style.display = 'block';

                    } else if (data.question.type === 'wordcloud') {
                        document.getElementById('question_options').innerHTML = `
                            <input type="text" id="answer1" name="word_cloud_response1" placeholder="Your first answer" />
                            <input type="text" id="answer2" name="word_cloud_response2" placeholder="Your second answer (optional)" />`;
                        document.getElementById('answer').style.display = 'none';

                    } else if (data.question.type === 'match_question') {
                        let leftOptions = "";
                        let rightOptions = "";

                        data.question.match_options.forEach((option) => {
                            leftOptions += `
                                <div class="flex-container">
                                    <div class="box left">${option}</div>
                                    <div class="dropzone-box dropzone"></div>
                                </div>`;
                        });

                        const shuffledAnswers = shuffleArray(data.question.match_answers);
                        shuffledAnswers.forEach(answer => {
                            rightOptions += `<div class="box draggable">${answer}</div>`;
                        });

                        document.getElementById('question_options').innerHTML = `
                            <div class="container">
                                ${leftOptions}
                               <div id="right" class="right">
                                    ${rightOptions}
                                </div>
                            </div>`;

                        document.getElementById('answer').style.display = 'none';

                        initializeDragAndDrop();
                        initializeSortable();
                    } else if (data.question.type === 'code_question') {
                        document.getElementById('question_options').innerHTML = `
                            <textarea id="code-editor"></textarea>
                            <button id="run-button" >Run Code</button>
                            <pre id="output"></pre>
                        `;

                        document.getElementById('answer').style.display = 'none';

                        let language = data.question.code_language || "python"; // Default to Python if null
                        let textarea = document.getElementById('code-editor');

                        // Initialize CodeMirror using imported function
                        let editor = initializeCodeEditor(textarea, language);

                        document.getElementById('run-button').addEventListener('click', function () {
                            executeCode(editor, language, 'output'); // Use imported function
                        });
                    }
                } else if (data.type === 'response_status') {
                    showFeedback(
                        data.success ? 'Response submitted successfully!' : "It seems like there's an invalid response, or this question might currently be locked. Please wait for the Lecturer to unlock it.",
                        data.success
                    );
                }
            };

            submitButton.addEventListener('click', function() {
                let responseData = null;

                switch (currentQuestionType) {
                    case 'multiple_choice':
                        responseData = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                            .map(cb => cb.value);
                        break;

                    case 'single_choice':
                        const selectedRadio = document.querySelector('input[name="single_choice"]:checked');
                        responseData = selectedRadio ? selectedRadio.value : null;
                        break;

                    case 'dropdown_fill':
                        const selectedOption = document.querySelector('select').value;
                        responseData = selectedOption || null;
                        break;

                    case 'text_fill':
                        responseData = document.getElementById('answer').value;
                        break;

                    case 'match_question':
                        responseData = Array.from(document.querySelectorAll('.flex-container')).map(container => {
                            const leftOption = container.querySelector('.left').textContent.trim();
                            const rightOptionElement = container.querySelector('.dropzone .box');
                            const rightOption = rightOptionElement ? rightOptionElement.textContent.trim() : null;
                            return {
                                left: leftOption,
                                right: rightOption
                            };
                        })

                        if (responseData.some(match => !match.right)) {
                            showFeedback('Please match all items before submitting.', false);
                            return;
                        }
                        break;

                    case 'wordcloud':
                        const answer1 = document.getElementById('answer1').value;
                        const answer2 = document.getElementById('answer2').value;
                        responseData = [answer1, answer2].filter(answer => answer !== '');
                        break;

                    case 'code_question':
                        // Get the CodeMirror instance from the text area
                        let codeEditor = document.querySelector('.CodeMirror'); // Get the CodeMirror container
                        if (codeEditor) {
                            let editorInstance = codeEditor.CodeMirror; // Access CodeMirror instance
                            responseData = editorInstance.getValue(); // Get the code inside the editor
                        } else {
                            console.error("CodeMirror instance not found.");
                            responseData = "";
                        }
                        break;
                }

                if (responseData && responseData.length !== 0) {
                    ws.send(JSON.stringify({
                        type: 'response',
                        question_id: currentQuestionId,
                        response_type: currentQuestionType,
                        response_data: responseData
                    }));
                } else {
                    showFeedback('Please provide a response', false);
                }
            });

            createLockOverlay();
        });