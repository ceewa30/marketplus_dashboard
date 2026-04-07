document.getElementById('period').addEventListener('change', function() {
    const period = this.value;
    const intervalSelect = document.getElementById('interval');
    const options = intervalSelect.options;

    // Define valid intervals for each period based on your rules
    const rules = {
        '1d':  ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d'],
        '5d':  ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d'],
        '1mo': ['2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '1wk', '1mo'],
        '3mo': ['60m', '1h', '1d', '1wk', '1mo', '3mo'],
        '6mo': ['60m', '1h', '1d', '1wk', '1mo', '3mo'],
        '1y':  ['60m', '1h', '1d', '1wk', '1mo', '3mo'],
        '3y':  ['1d', '1wk', '1mo', '3mo'],
        '5y':  ['1d', '1wk', '1mo', '3mo'],
        '10y': ['1d', '1wk', '1mo', '3mo']
    };

    const validIntervals = rules[period] || [];
    let firstValidSet = false;

    for (let i = 0; i < options.length; i++) {
        const opt = options[i];
        if (validIntervals.includes(opt.value)) {
            opt.disabled = false;
            opt.style.display = 'block';
            // Auto-select the first valid option if current selection becomes invalid
            if (!firstValidSet) {
                if (!validIntervals.includes(intervalSelect.value)) {
                    intervalSelect.value = opt.value;
                }
                firstValidSet = true;
            }
        } else {
            opt.disabled = true;
            opt.style.display = 'none';
        }
    }
});

// Trigger once on page load to set initial state
document.getElementById('period').dispatchEvent(new Event('change'));