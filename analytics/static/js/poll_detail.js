document.addEventListener("DOMContentLoaded", function () {
    // Configuration and state
    const config = {
        colors: {
            regular: {
                pie: {
                    border: '#3d073e',
                    background: generateRandomColor
                },
                bar: {
                    border: '#3d073e',
                    background: '#800080'
                },
                line: {
                    border: '#3d073e',
                    background: '#b833ff'
                }
            },
            correct: {
                map: {
                    'Correct Responses': '#64b164',
                    'Incorrect Responses': '#da4949'
                },
                border: '#171717'
            }
        }
    };

    const elements = {
        chart: document.getElementById('chart'),
        ctx: document.getElementById('chart').getContext('2d'),
        noDataMessage: document.getElementById('no-data-message'),
        questionTitle: document.getElementById('selected-question-title'),
        responseCountContainer: document.querySelector('.button-container'),
        correctAnswerContainer: document.querySelector('.correct-answer-btn-container'),
        lineGraphButton: document.getElementById('viewLineGraph'),
        csrfToken: document.querySelector('[name=csrfmiddlewaretoken]').value,
        pollId: document.getElementById("poll-data").getAttribute("data-poll-id")
    };

    const state = {
        chartInstance: null,
        selectedQuestionId: null,
        isCorrectAnalytics: false
    };

    const buttons = {
        viewPieChart: () => renderChart('pie'),
        viewBarGraph: () => renderChart('bar'),
        viewLineGraph: () => renderChart('line'),
        viewPollResults: () => {
            state.isCorrectAnalytics = false;
            state.selectedQuestionId = null;
            elements.questionTitle.innerText = "Poll Response Count Results";
            renderChart('pie');
            updateUI();
        },
        viewCorrectPieChart: () => renderChart('pie'),
        viewCorrectBarGraph: () => renderChart('bar'),
        viewCorrectAnalytics: () => {
            state.isCorrectAnalytics = true;
            state.selectedQuestionId = null;
            elements.questionTitle.innerText = "Poll Correct Response Results";
            renderChart('pie');
            updateUI();
        }
    };

    function clearChart() {
        if (state.chartInstance) {
            state.chartInstance.destroy();
        }
    }

    function generateRandomColor() {
        const hueRanges = [[200, 250], [260, 290], [300, 340]]; // Blue, purple and pink colour scheme
        const selectedRange = hueRanges[Math.floor(Math.random() * hueRanges.length)];
        const hue = Math.floor(Math.random() * (selectedRange[1] - selectedRange[0]) + selectedRange[0]);
        const saturation = Math.floor(Math.random() * (80 - 50) + 50); // 50% - 80% saturation
        const lightness = Math.floor(Math.random() * (75 - 40) + 40);  // 40% - 75% lightness
        return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    }

    function updateUI() {
        elements.responseCountContainer.style.display = state.isCorrectAnalytics ? 'none' : 'flex';
        elements.correctAnswerContainer.style.display = state.isCorrectAnalytics ? 'flex' : 'none';

        elements.lineGraphButton.style.display = state.selectedQuestionId ? 'none' : 'block';
    }

    function handleNoData(dataArray) {
        if (!dataArray || dataArray.length === 0 || dataArray.every(num => num === 0)) {
            elements.chart.style.display = 'none';
            elements.noDataMessage.style.display = 'block';
            return true;
        } else {
            elements.chart.style.display = 'block';
            elements.noDataMessage.style.display = 'none';
            return false;
        }
    }

    function fetchChartData(chartType) {
        let url;

        if (state.isCorrectAnalytics) {
            if (chartType === 'pie') {
                url = state.selectedQuestionId
                    ? `/analytics/questions/${state.selectedQuestionId}/correct_analytics/`
                    : `/analytics/polls/${elements.pollId}/correct_piechart_data/`;
            } else if (chartType === 'bar') {
                url = state.selectedQuestionId
                    ? `/analytics/questions/${state.selectedQuestionId}/correct_analytics/`
                    : `/analytics/polls/${elements.pollId}/correct_bargraph_data/`;
            }
        } else {
            if (chartType === 'pie') {
                url = state.selectedQuestionId
                    ? `/analytics/questions/${state.selectedQuestionId}/analytics/?type=pie`
                    : `/analytics/polls/${elements.pollId}/piechart_data/`;
            } else if (chartType === 'bar') {
                url = state.selectedQuestionId
                    ? `/analytics/questions/${state.selectedQuestionId}/analytics/?type=bar`
                    : `/analytics/polls/${elements.pollId}/bargraph_data/`;
            } else if (chartType === 'line') {
                url = state.selectedQuestionId
                    ? `/analytics/questions/${state.selectedQuestionId}/analytics/?type=line`
                    : `/analytics/polls/${elements.pollId}/linegraph_data/`;
            }
        }

        return fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': elements.csrfToken
            }
        })
        .then(response => response.json())
        .catch(error => {
            console.error(`Error fetching ${chartType} chart data:`, error);
            return { labels: [], data: [] };
        });
    }

    function renderChart(chartType) {
        clearChart();

        fetchChartData(chartType).then(data => {
            if (handleNoData(data.data)) return; // If no data, stop here
            const chartConfig = createChartConfig(chartType, data); // Create chart config based on type and mode
            state.chartInstance = new Chart(elements.ctx, chartConfig); // Create chart
        });
    }

    function createChartConfig(chartType, data) {
        const baseConfig = { // Base configuration for all chart types
            responsive: true,
            maintainAspectRatio: false
        };

        const chartTitle = getChartTitle(chartType); // Chart title based on type and selected question

        // Create chart-specific configuration
        if (state.isCorrectAnalytics) {
            return createCorrectAnalyticsChartConfig(chartType, data, baseConfig, chartTitle);
        } else {
            return createRegularChartConfig(chartType, data, baseConfig, chartTitle);
        }
    }

    function getChartTitle(chartType) {
        const isQuestionSpecific = state.selectedQuestionId !== null;

        if (state.isCorrectAnalytics) {
            return isQuestionSpecific
                ? `Correct vs Incorrect Responses (${chartType.charAt(0).toUpperCase() + chartType.slice(1)} Chart)`
                : "Total Correct vs Incorrect Responses" + (chartType === 'bar' ? " (Bar Chart)" : "");
        } else {
            return isQuestionSpecific
                ? `Responses (${chartType.charAt(0).toUpperCase() + chartType.slice(1)} Graph)`
                : `Total Number of Responses${chartType !== 'pie' ? ` (${chartType.charAt(0).toUpperCase() + chartType.slice(1)} Graph)` : ""}`;
        }
    }

    function createCorrectAnalyticsChartConfig(chartType, data, baseConfig, chartTitle) {
        const colorMap = config.colors.correct.map;
        const borderColor = config.colors.correct.border;

        if (chartType === 'pie') {
            return {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: data.labels.map(label => colorMap[label]),
                        borderColor: borderColor,
                        borderWidth: 2
                    }]
                },
                options: {
                    ...baseConfig,
                    plugins: {
                        title: {
                            display: true,
                            text: chartTitle,
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
                            bodyFont: { size: 12 },
                            titleFont: { size: 14 }
                        }
                    }
                }
            };
        } else if (chartType === 'bar') {
            return {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: data.labels.map(label => colorMap[label]),
                        borderColor: borderColor,
                        borderWidth: 3
                    }]
                },
                options: {
                    ...baseConfig,
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
                        legend: { display: false },
                        title: {
                            display: true,
                            text: chartTitle,
                            font: { size: 22, weight: 'bold' }
                        }
                    }
                }
            };
        }
    }

    function createRegularChartConfig(chartType, data, baseConfig, chartTitle) {
        if (chartType === 'pie') {
            return {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: data.labels.map(() => generateRandomColor()),
                        borderColor: config.colors.regular.pie.border,
                        borderWidth: 2
                    }]
                },
                options: {
                    ...baseConfig,
                    plugins: {
                        title: {
                            display: true,
                            text: chartTitle,
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
                            bodyFont: { size: 12 },
                            titleFont: { size: 14 }
                        }
                    }
                }
            };
        } else if (chartType === 'bar') {
            return {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: config.colors.regular.bar.background,
                        borderColor: config.colors.regular.bar.border,
                        borderWidth: 2
                    }]
                },
                options: {
                    ...baseConfig,
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
                        legend: { display: false },
                        title: {
                            display: true,
                            text: chartTitle,
                            font: { size: 22, weight: 'bold' }
                        }
                    }
                }
            };
        } else if (chartType === 'line') {
            return {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Responses',
                        data: data.data,
                        backgroundColor: config.colors.regular.line.background,
                        borderColor: config.colors.regular.line.border,
                        fill: false
                    }]
                },
                options: {
                    ...baseConfig,
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
                            text: chartTitle,
                            font: { size: 22, weight: 'bold' }
                        }
                    }
                }
            };
        }
    }

    function initEventListeners() {
        Object.keys(buttons).forEach(buttonId => {
            const button = document.getElementById(buttonId);
            if (button) {
                button.addEventListener('click', buttons[buttonId]);
            }
        });

        // Question item click events
        document.querySelectorAll('.question-item').forEach((item, index) => {
            item.addEventListener('click', function () {
                state.selectedQuestionId = this.getAttribute('data-question-id');

                // Update title
                const questionNumber = `Q${index + 1}`;
                const questionText = this.innerText
                    .replace(questionNumber, '')
                    .replace('View Analytics', '')
                    .trim();

                elements.questionTitle.innerText = `Analytics for ${questionNumber} ${questionText}`;

                renderChart('pie'); // Show appropriate chart

                updateUI();
            });
        });
    }

    function init() {
        initEventListeners();
        renderChart('pie'); // Default to pie chart on load
        updateUI();
    }

    init(); // Start
});