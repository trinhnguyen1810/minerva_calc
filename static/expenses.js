document.addEventListener('DOMContentLoaded', function() {
    var categories = ['Groceries/Food', 'Transportation', 'Entertainment', 'Health & Fitness', 'Miscellaneous', 'Loans Payments', 'Other expenses'];
    var amounts = [200, 100, 50, 50, 100, 300, 150];
    var colors = ['#ff5733', '#ffc300', '#c70039', '#900c3f', '#ff5733', '#ff5733', '#ffc300'];

    var ctx = document.getElementById('expenseChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categories,
            datasets: [{
                data: amounts,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                position: 'right',
                labels: {
                    padding: 20,
                    boxWidth: 12
                }
            },
            title: {
                display: true,
                text: 'Expense Allocation'
            }
        }
    });
});
