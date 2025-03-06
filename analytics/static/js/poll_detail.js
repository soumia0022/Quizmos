
document.addEventListener("DOMContentLoaded", function () {
    var ctx = document.getElementById('chart').getContext('2d');
    var chartInstance = null;
    var selectedQuestionId = null; // Track selected question
    var pollId = document.getElementById("poll-data").getAttribute("data-poll-id"); // Get poll ID from HTML

    function clearChart() {
        if (chartInstance) {
            chartInstance.destroy();
        }
    }

    function generateRandomColor() {
        const hueRanges = [[200, 250], [260, 290], [300, 340]];
        const selectedRange = hueRanges[Math.floor(Math.random() * hueRanges.length)];
        const hue = Math.floor(Math.random() * (selectedRange[1] - selectedRange[0]) + selectedRange[0]);
        return `hsl(${hue}, 60%, 60%)`;
    }

    function showPieChart() {
        clearChart();
        let url = selectedQuestionId
            ? `/analytics/questions/${selectedQuestionId}/analytics/?type=pie`
            : `/analytics/polls/${pollId}/piechart_data/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                chartInstance = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.data,
                            backgroundColor: data.labels.map(() => generateRandomColor()),
                            borderColor: '#3d073e',
                            borderWidth: 2
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            })
            .catch(error => console.error("Error fetching pie chart data:", error));
    }

    function showBarGraph() {
        clearChart();
        let url = selectedQuestionId
            ? `/analytics/questions/${selectedQuestionId}/analytics/?type=bar`
            : `/analytics/polls/${pollId}/bargraph_data/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                chartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Responses',
                            data: data.data,
                            backgroundColor: "#800080",
                            borderColor: '#3d073e',
                            borderWidth: 2
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            })
            .catch(error => console.error("Error fetching bar chart data:", error));
    }

    function showLineGraph() {
        clearChart();
        let url = selectedQuestionId
            ? `/analytics/questions/${selectedQuestionId}/analytics/?type=line`
            : `/analytics/polls/${pollId}/linegraph_data/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                chartInstance = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Responses',
                            data: data.data,
                            backgroundColor: "#b833ff",
                            borderColor: "#3d073e",
                            fill: false
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            })
            .catch(error => console.error("Error fetching line graph data:", error));
    }

    function toggleLineGraphButton() {
        document.getElementById('viewLineGraph').style.display = selectedQuestionId ? 'none' : 'block';
    }

    function showPollResults() {
        selectedQuestionId = null;
        document.getElementById('selected-question-title').innerText = "Poll Results";
        showPieChart();
        toggleLineGraphButton();
    }

    document.querySelectorAll('.question-item').forEach((item, index) => {
        item.addEventListener('click', function () {
            selectedQuestionId = this.getAttribute('data-question-id');
            let questionNumber = `Q${index + 1}`;
            let questionText = this.innerText.replace(questionNumber, '').replace('View Analytics', '').trim();
            document.getElementById('selected-question-title').innerText = `Analytics for ${questionNumber}: ${questionText}`;
            showPieChart();
            toggleLineGraphButton();
        });
    });

    document.getElementById('viewPieChart').addEventListener('click', showPieChart);
    document.getElementById('viewBarGraph').addEventListener('click', showBarGraph);
    document.getElementById('viewLineGraph').addEventListener('click', showLineGraph);
    document.getElementById('viewPollResults').addEventListener('click', showPollResults);

    showPieChart();
    toggleLineGraphButton();
});
