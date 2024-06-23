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

    // Function to create a chart
    function createChart(data, type = 'line') {
        var ctx = document.getElementById("stock-chart").getContext("2d");
        if (window.stockChart) {
            window.stockChart.destroy();
        }

        var chartType = (type === 'bar') ? 'bar' : 'line';
        var gradientStroke = ctx.createLinearGradient(0, 500, 0, 0); // Adjusted vertical positions
        gradientStroke.addColorStop(1, 'rgba(23, 193, 232, 0.3)'); // Increased opacity
        gradientStroke.addColorStop(0.8, 'rgba(23, 193, 232, 0.2)');
        gradientStroke.addColorStop(0.5, 'rgba(23, 193, 232, 0.1)');
        gradientStroke.addColorStop(0.3, 'rgba(23, 193, 232, 0.05)');
        gradientStroke.addColorStop(0, 'rgba(23, 193, 232, 0.02)');

        window.stockChart = new Chart(ctx, {
            type: chartType,
            data: {
                datasets: [{
                    label: (chartType === 'line') ? 'Stock Data' : 'Volume Data',
                    data: data,
                    borderColor: '#17c1e8', // Border color for the line or bar
                    backgroundColor: (chartType === 'line') ? gradientStroke : '#17c1e8', // Background color for line or bar
                    borderWidth: (chartType === 'line') ? 3 : 0,
                    fill: (chartType === 'line') ? true : false,
                    pointRadius: 0,
                    tension: 0.4,
                    borderRadius: 4
                }]
            },
            options: {
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'month'
                        },
                        grid: {
                            drawBorder: false,
                            display: false,
                            drawOnChartArea: false,
                            drawTicks: false,
                            borderDash: [5, 5]
                        },
                        ticks: {
                            display: true,
                            color: '#b2b9bf',
                            padding: 10,
                            font: {
                                size: 11,
                                family: 'Open Sans',
                                style: 'normal',
                                lineHeight: 2
                            }
                        }
                    },
                    y: {
                        grid: {
                            drawBorder: false,
                            display: true,
                            drawOnChartArea: true,
                            drawTicks: false,
                            borderDash: [5, 5]
                        },
                        ticks: {
                            display: true,
                            padding: 10,
                            color: '#b2b9bf',
                            font: {
                                size: 11,
                                family: 'Open Sans',
                                style: 'normal',
                                lineHeight: 2
                            }
                        }
                    }
                }
            }
        });

        // Update chart dimensions after creating it
        updateChartDimensions();
    }

    // Function to update chart dimensions based on viewport
    function updateChartDimensions() {
        var chartCanvas = document.getElementById('stock-chart');
        var parentContainer = chartCanvas.parentElement;

        // Set canvas height based on parent container's computed height
        var computedHeight = window.getComputedStyle(parentContainer).height;
        chartCanvas.style.height = computedHeight;
        window.stockChart.resize(); // Resize the chart after setting new dimensions
    }

    // Initial chart with Price dataset
    createChart(datasets.Price);

    // Dropdown change event
    document.querySelectorAll('.dropdown-item').forEach(function(item) {
        item.addEventListener('click', function() {
            var selectedGraph = this.getAttribute('data-graph');
            document.getElementById('dropdownMenuButton').textContent = this.textContent; // Update dropdown button text
            if (selectedGraph === 'Volume') {
                createChart(datasets[selectedGraph], 'bar'); // Create bar chart for Volume
            } else {
                createChart(datasets[selectedGraph]); // Default to line chart for other datasets
            }
        });
    });

    // Resize chart on window resize
    window.addEventListener('resize', function() {
        updateChartDimensions();
    });
});
