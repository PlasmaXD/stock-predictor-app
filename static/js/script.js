function fetchSymbols() {
    fetch('/symbols')
        .then(response => response.json())
        .then(data => {
            const symbolList = document.getElementById('symbolList');
            symbolList.innerHTML = '';
            data.symbols.forEach(symbol => {
                const symbolDiv = document.createElement('div');
                symbolDiv.className = 'symbol';
                symbolDiv.textContent = symbol;
                symbolDiv.addEventListener('click', () => getPrediction(symbol));
                symbolList.appendChild(symbolDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}

function getPrediction(symbol) {
    document.getElementById('selectedSymbol').textContent = `Selected Symbol: ${symbol}`;
    fetch(`/predict?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('predictionResult').textContent = `Error: ${data.error}`;
                return;
            }
            displayPrediction(data, symbol);
        })
        .catch(error => console.error('Error:', error));
}

function displayPrediction(data, symbol) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    const predictions = data.prices.map(item => item[0]);
    const labels = data.dates;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${symbol} Stock Price Prediction`,
                data: predictions,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        tooltipFormat: 'MMM dd, yyyy'
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Stock Price'
                    }
                }
            }
        }
    });
}
