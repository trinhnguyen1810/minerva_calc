// Expenses chart initialization
document.addEventListener('DOMContentLoaded', function() {
    const chartData = JSON.parse(document.getElementById('chart-data').textContent);
    
    // Create a pie chart using Chart.js
    const ctx = document.getElementById('expenses-chart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartData.labels,
            datasets: [{
                data: chartData.values,
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 20,
                        boxWidth: 12
                    }
                },
                title: {
                    display: true,
                    text: 'Budget Allocation',
                    font: {
                        size: 20
                    }
                }
            }
        }
    });
});
