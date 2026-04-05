// Dashboard JavaScript for charts and visualizations

document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    initProcessedImagesChart();
    initGradeDistributionChart();
    initPriceHistoryChart();
    
    // Set up refresh button
    const refreshBtn = document.getElementById('refresh-dashboard');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            // Show loading state
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Refreshing...';
            this.disabled = true;
            
            // Refresh all charts
            Promise.all([
                updateProcessedImagesChart(),
                updateGradeDistributionChart(),
                updatePriceHistoryChart()
            ]).then(() => {
                // Reset button state
                this.innerHTML = '<i class="feather feather-refresh-cw"></i> Refresh Data';
                this.disabled = false;
            }).catch(error => {
                console.error('Error refreshing dashboard data:', error);
                this.innerHTML = '<i class="feather feather-refresh-cw"></i> Refresh Data';
                this.disabled = false;
            });
        });
    }
});

// Chart objects to allow updates
let processedImagesChart = null;
let gradeDistributionChart = null;
let priceHistoryChart = null;

// Initialize processed images chart
function initProcessedImagesChart() {
    fetch('/api/statistics/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('processed-images-chart');
            if (!ctx) return;
            
            processedImagesChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Images Processed',
                        data: data.data,
                        backgroundColor: 'rgba(76, 175, 80, 0.2)',
                        borderColor: 'rgba(76, 175, 80, 1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                title: function(tooltipItems) {
                                    return 'Date: ' + tooltipItems[0].label;
                                },
                                label: function(context) {
                                    return 'Images: ' + context.raw;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching statistics:', error));
}

// Initialize grade distribution chart
function initGradeDistributionChart() {
    fetch('/api/grade-distribution/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('grade-distribution-chart');
            if (!ctx) return;
            
            // Generate colors for each grade
            const colors = generateColors(data.labels.length);
            
            gradeDistributionChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: colors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = Math.round((value / total) * 100);
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching grade distribution:', error));
}

// Initialize price history chart
function initPriceHistoryChart() {
    fetch('/api/price-history/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('price-history-chart');
            if (!ctx) return;
            
            priceHistoryChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Average Price',
                        data: data.data,
                        backgroundColor: 'rgba(130, 119, 23, 0.6)',
                        borderColor: 'rgba(130, 119, 23, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toFixed(2);
                                }
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return 'Avg Price: $' + context.raw.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching price history:', error));
}

// Update processed images chart
function updateProcessedImagesChart() {
    return fetch('/api/statistics/')
        .then(response => response.json())
        .then(data => {
            if (processedImagesChart) {
                processedImagesChart.data.labels = data.labels;
                processedImagesChart.data.datasets[0].data = data.data;
                processedImagesChart.update();
            }
        });
}

// Update grade distribution chart
function updateGradeDistributionChart() {
    return fetch('/api/grade-distribution/')
        .then(response => response.json())
        .then(data => {
            if (gradeDistributionChart) {
                // Generate new colors if number of grades has changed
                if (gradeDistributionChart.data.labels.length !== data.labels.length) {
                    const colors = generateColors(data.labels.length);
                    gradeDistributionChart.data.datasets[0].backgroundColor = colors;
                }
                
                gradeDistributionChart.data.labels = data.labels;
                gradeDistributionChart.data.datasets[0].data = data.data;
                gradeDistributionChart.update();
            }
        });
}

// Update price history chart
function updatePriceHistoryChart() {
    return fetch('/api/price-history/')
        .then(response => response.json())
        .then(data => {
            if (priceHistoryChart) {
                priceHistoryChart.data.labels = data.labels;
                priceHistoryChart.data.datasets[0].data = data.data;
                priceHistoryChart.update();
            }
        });
}

// Generate colors for charts
function generateColors(count) {
    const colors = [];
    const baseColors = [
        'rgba(76, 175, 80, 0.8)',    // Green
        'rgba(130, 119, 23, 0.8)',   // Olive
        'rgba(33, 150, 243, 0.8)',   // Blue
        'rgba(255, 152, 0, 0.8)',    // Orange
        'rgba(156, 39, 176, 0.8)',   // Purple
        'rgba(233, 30, 99, 0.8)',    // Pink
        'rgba(0, 188, 212, 0.8)',    // Cyan
        'rgba(205, 220, 57, 0.8)'    // Lime
    ];
    
    // Repeat base colors if there are more categories than colors
    for (let i = 0; i < count; i++) {
        colors.push(baseColors[i % baseColors.length]);
    }
    
    return colors;
}
