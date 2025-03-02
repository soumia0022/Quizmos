export function startCountdownTimer(questionElement, initialSeconds) {
  let remainingSeconds = parseInt(initialSeconds, 10);

  let timerElement = questionElement.querySelector('.question-timer');

  // function to update the timer display
  function updateTimerDisplay() {
    timerElement.textContent = `Time remaining: ${getFormattedTime(remainingSeconds)}`;
  }

  // set up the interval to count down
  const timerInterval = setInterval(() => {
    remainingSeconds--;
    updateTimerDisplay();

    // when time runs out
    if (remainingSeconds <= 0) {
      clearInterval(timerInterval);
      timerElement.textContent = "Time's up!";

      handleTimerExpired(questionElement);
    }
  }, 1000);

  return timerInterval;
}
export function getFormattedTime(seconds){
  const minutes = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return `${minutes.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
}

// Handle what happens when the timer expires
function handleTimerExpired(questionElement) {


  //add a message
  const messageElement = document.createElement('div');
  messageElement.className = 'timer-expired-message';
  messageElement.textContent = 'Time expired!';
  questionElement.appendChild(messageElement);
}

window.startCountdownTimer = startCountdownTimer;
