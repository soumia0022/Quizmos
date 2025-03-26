export function updateProgressBar(currentNum, total) {
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