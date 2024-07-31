document.addEventListener('DOMContentLoaded', function() {
    console.log("Getting stock data");

    // Extract stock data from global variable
    var stock = stockData;
    console.log(stock);

    // Extract datasets with x and y values
    var datasets = {
        Price: stock.graph_data.Price.map(item => ({ x: item.Date, y: parseFloat(item.Value) })),
        DMA50: stock.graph_data.DMA50.map(item => ({ x: item.Date, y: parseFloat(item.Value) })),
        DMA200: stock.graph_data.DMA200.map(item => ({ x: item.Date, y: parseFloat(item.Value) })),
        Volume: stock.graph_data.Volume.map(item => ({ x: item.Date, y: parseFloat(item.Value) }))
    };

    // Color configuration for datasets
    const colors = {
        Price: '#17c1e8',
        DMA50: '#ff9800',
        DMA200: '#f44336',
        Volume: '#4caf50'
    };

    // Function to create a chart
    function createChart() {
        var ctx = document.getElementById("stock-chart").getContext("2d");
        if (window.stockChart) {
            window.stockChart.destroy();
        }

        var activeDatasets = [
            {
                label: 'Price',
                data: datasets.Price,
                borderColor: colors.Price,
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4,
                type: 'line',
                yAxisID: 'y-price',
                order: 0
            },
            {
                label: 'DMA50',
                data: datasets.DMA50,
                borderColor: colors.DMA50,
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4,
                type: 'line',
                yAxisID: 'y-price',
                order: 0
            },
            {
                label: 'DMA200',
                data: datasets.DMA200,
                borderColor: colors.DMA200,
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4,
                type: 'line',
                yAxisID: 'y-price',
                order: 0
            },
            {
                label: 'Volume',
                data: datasets.Volume,
                borderColor: colors.Volume,
                backgroundColor: colors.Volume + '80',
                borderWidth: 0,
                pointRadius: 0,
                tension: 0.4,
                type: 'bar',
                yAxisID: 'y-volume',
                order: 1
            }
        ];

        window.stockChart = new Chart(ctx, {
            data: { datasets: activeDatasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: { unit: 'month' },
                        grid: { display: false },
                        ticks: {
                            color: '#666',
                            font: { size: 12 }
                        }
                    },
                    'y-price': {
                        position: 'left',
                        grid: {
                            color: '#e0e0e0',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#666',
                            font: { size: 12 }
                        }
                    },
                    'y-volume': {
                        position: 'right',
                        grid: { display: false },
                        ticks: {
                            color: '#666',
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }

    // Initial chart creation
    createChart();

    // Resize chart on window resize
    window.addEventListener('resize', function() {
        if (window.stockChart) {
            window.stockChart.resize();
        }
    });
});
