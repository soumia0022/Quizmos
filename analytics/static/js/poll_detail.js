// This file requires refactoring

document.addEventListener("DOMContentLoaded", function () {
    var ctx = document.getElementById('chart').getContext('2d');
    var chartInstance = null;
    var selectedQuestionId = null; // Track selected question
    var pollId = document.getElementById("poll-data").getAttribute("data-poll-id"); // Get poll ID from HTML
    var isCorrectAnalytics = false; // Flag to track which analytics mode we're in

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

    function toggleButtonContainers() {
        const responseCountContainer = document.querySelector('.button-container');
        const correctAnswerContainer = document.querySelector('.correct-answer-btn-container');

        if (isCorrectAnalytics) {
            responseCountContainer.style.display = 'none';
            correctAnswerContainer.style.display = 'flex';
        } else {
            responseCountContainer.style.display = 'flex';
            correctAnswerContainer.style.display = 'none';
        }
    }

    function showCorrectPieChart() {
        clearChart();
        let url = selectedQuestionId
            ? `/analytics/questions/${selectedQuestionId}/correct_analytics/`
            : `/analytics/polls/${pollId}/correct_piechart_data/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const colourMap = {
                    'Correct Responses': '#64b164',   // Bright green
                    'Incorrect Responses': '#da4949', // Bright red
                };
                chartInstance = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.data,
                            backgroundColor: data.labels.map(label => colourMap[label]),
                            borderColor: '#171717',
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
                                    ? `Correct vs Incorrect Responses (Pie Chart)`
                                    : "Total Correct vs Incorrect Responses",
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
            .catch(error => console.error("Error fetching correct pie chart data:", error));
    }

    function showCorrectBarGraph() {
        clearChart();
        let url = selectedQuestionId
            ? `/analytics/questions/${selectedQuestionId}/correct_analytics/`
            : `/analytics/polls/${pollId}/correct_bargraph_data/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const colourMap = {
                    'Correct Responses': '#64b164',
                    'Incorrect Responses': '#da4949',
                };
                chartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.data,
                            backgroundColor: data.labels.map(label => colourMap[label]),
                            borderColor: '#171717',
                            borderWidth: 3
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
                            legend: {
                                display: false // Remove legend
                            },
                            title: {
                                display: true,
                                text: selectedQuestionId
                                    ? `Correct vs Incorrect Responses (Bar Graph)`
                                    : "Total Correct vs Incorrect Responses (Bar Chart)",
                                font: { size: 22, weight: 'bold' }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error("Error fetching correct bar chart data:", error));
    }

    function showCorrectResults() {
        isCorrectAnalytics = true;
        selectedQuestionId = null; // Reset to poll-wide correct analytics
        document.getElementById('selected-question-title').innerText = "Poll Correct Response Results";
        toggleButtonContainers();
        showCorrectPieChart(); // Shows poll-wide correct pie chart
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
        let url;

        // Explicitly choose the URL based on the current state
        if (isCorrectAnalytics) {
            url = selectedQuestionId
                ? `/analytics/questions/${selectedQuestionId}/correct_analytics/`
                : `/analytics/polls/${pollId}/correct_bargraph_data/`;
        } else {
            url = selectedQuestionId
                ? `/analytics/questions/${selectedQuestionId}/analytics/?type=bar`
                : `/analytics/polls/${pollId}/bargraph_data/`;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                chartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
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
                            legend: {
                                display: false // Remove legend
                            },
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
        isCorrectAnalytics = false;
        selectedQuestionId = null; // Reset question selection
        document.getElementById('selected-question-title').innerText = "Poll Response Count Results";
        showPieChart();
        toggleLineGraphButton();
        toggleButtonContainers();
    }

    // Load pie chart automatically when question is clicked
    document.querySelectorAll('.question-item').forEach((item, index) => {
        item.addEventListener('click', function () {
            selectedQuestionId = this.getAttribute('data-question-id');
            let questionNumber = `Q${index + 1}`;
            let questionText = this.innerText.replace(questionNumber, '').replace('View Analytics', '').trim();

            document.getElementById('selected-question-title').innerText = `Analytics for ${questionNumber} ${questionText}`;

            // If in correct analytics mode, show correct analytics for the specific question
            if (isCorrectAnalytics) {
                showCorrectPieChart();
            } else {
                // Otherwise, show regular response analytics
                showPieChart();
            }

            toggleButtonContainers();
        });
    });

    document.getElementById('viewPieChart').addEventListener('click', showPieChart);
    document.getElementById('viewBarGraph').addEventListener('click', showBarGraph);
    document.getElementById('viewLineGraph').addEventListener('click', showLineGraph);
    document.getElementById('viewPollResults').addEventListener('click', showPollResults);

    document.getElementById('viewCorrectPieChart').addEventListener('click', showCorrectPieChart);
    document.getElementById('viewCorrectBarGraph').addEventListener('click', showCorrectBarGraph);
    document.getElementById('viewCorrectAnalytics').addEventListener('click', showCorrectResults);

    showPieChart();
    toggleButtonContainers();
});