// This file requires some refactoring

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
        const hueRanges = [[200, 250], [260, 290], [300, 340]]; // Blue, purple and pink colour scheme
        const selectedRange = hueRanges[Math.floor(Math.random() * hueRanges.length)];
        const hue = Math.floor(Math.random() * (selectedRange[1] - selectedRange[0]) + selectedRange[0]);
        const saturation = Math.floor(Math.random() * (80 - 50) + 50); // 50% - 80% saturation
        const lightness = Math.floor(Math.random() * (75 - 40) + 40);  // 40% - 75% lightness
        return `hsl(${hue}, ${saturation}%, ${lightness}%)`; // Convert HSL to CSS format
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
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: selectedQuestionId
                                    ? `Responses (Pie Chart)`
                                    : "Total Number of Responses",
                                font: {size: 22, weight: 'bold'},
                            },
                            legend: {
                                display: true,
                                labels: {
                                    font: {size: 15},
                                    padding: 12,
                                    boxWidth: 20,
                                },
                            },
                            tooltip: {
                                bodyFont: {
                                    size: 12
                                },
                                titleFont: {
                                    size: 14
                                }
                            }
                        }
                    }
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
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: { font: { size: 14 } }
                            },
                            x: {
                                ticks: { font: { size: 14 } }
                            }
                        },
                        plugins: {
                            title: {
                                display: true,
                                text: selectedQuestionId
                                    ? `Responses (Bar Graph)`
                                    : "Total Number of Responses (Bar Chart)",
                                font: { size: 22, weight: 'bold' }
                            }
                        }
                    }
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
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: { font: { size: 14 } }
                            },
                            x: {
                                ticks: { font: { size: 14 } }
                            }
                        },
                         plugins: {
                            title: {
                                display: true,
                                text: selectedQuestionId
                                    ? `Responses (Line Graph)`
                                    : "Total Number of Responses (Line Graph)",
                                font: { size: 22, weight: 'bold' }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error("Error fetching line graph data:", error));
    }

    function toggleLineGraphButton() {
        document.getElementById('viewLineGraph').style.display = selectedQuestionId ? 'none' : 'block';
    }

    function showPollResults() {
        selectedQuestionId = null; // Reset question selection
        document.getElementById('selected-question-title').innerText = "Poll Results";
        showPieChart();
        toggleLineGraphButton();
    }

    // Load pie chart automatically when question is clicked
    document.querySelectorAll('.question-item').forEach((item, index) => {
        item.addEventListener('click', function () {
            selectedQuestionId = this.getAttribute('data-question-id');
            let questionNumber = `Q${index + 1}`;
            let questionText = this.innerText.replace(questionNumber, '').replace('View Analytics', '').trim();
            document.getElementById('selected-question-title').innerText = `Analytics for ${questionNumber} ${questionText}`;
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
