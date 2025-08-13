// Dashboard Auto-Updater
// Updates prices from latest_prices.json file

async function updateDashboardPrices() {
    try {
        // Fetch latest prices
        const response = await fetch('data/latest_prices.json');
        const prices = await response.json();
        
        // Update positions table
        updatePositionPrices(prices);
        
        // Update portfolio summary
        updatePortfolioSummary(prices);
        
        // Update benchmark comparison
        updateBenchmarks(prices);
        
        // Update last refresh time
        updateLastRefreshTime();
        
    } catch (error) {
        console.error('Error updating prices:', error);
    }
}

function updatePositionPrices(prices) {
    // Original entry prices (keep these constant)
    const positions = {
        'CHPT': { qty: 26, entry: 10.7845 },
        'EVGO': { qty: 82, entry: 3.6271 },
        'FCEL': { qty: 97, entry: 4.05 }
    };
    
    let totalValue = 0;
    let totalPnL = 0;
    
    // Update each position row
    Object.keys(positions).forEach(symbol => {
        if (prices[symbol]) {
            const pos = positions[symbol];
            const currentPrice = prices[symbol].price;
            const marketValue = pos.qty * currentPrice;
            const cost = pos.qty * pos.entry;
            const pnl = marketValue - cost;
            const pnlPercent = (pnl / cost) * 100;
            
            totalValue += marketValue;
            totalPnL += pnl;
            
            // Update table cells (if elements exist)
            const row = document.querySelector(`tr[data-symbol="${symbol}"]`);
            if (row) {
                row.querySelector('.current-price').textContent = `$${currentPrice.toFixed(2)}`;
                row.querySelector('.market-value').textContent = `$${marketValue.toFixed(2)}`;
                row.querySelector('.pnl').textContent = `${pnl >= 0 ? '+' : ''}$${pnl.toFixed(2)}`;
                row.querySelector('.pnl-percent').textContent = `${pnl >= 0 ? '+' : ''}${pnlPercent.toFixed(2)}%`;
                
                // Update color based on P&L
                const pnlCells = row.querySelectorAll('.pnl, .pnl-percent');
                pnlCells.forEach(cell => {
                    cell.className = pnl >= 0 ? 'text-green-600 font-medium' : 'text-red-600 font-medium';
                });
            }
        }
    });
    
    // Update totals row
    const totalRow = document.querySelector('tr.bg-gray-50');
    if (totalRow) {
        totalRow.querySelector('td:nth-child(5)').textContent = `$${totalValue.toFixed(2)}`;
        totalRow.querySelector('td:nth-child(6)').textContent = `${totalPnL >= 0 ? '+' : ''}$${totalPnL.toFixed(2)}`;
        totalRow.querySelector('td:nth-child(7)').textContent = `${totalPnL >= 0 ? '+' : ''}${((totalPnL / 970.67) * 100).toFixed(2)}%`;
    }
}

function updatePortfolioSummary(prices) {
    const positions = {
        'CHPT': { qty: 26, entry: 10.7845 },
        'EVGO': { qty: 82, entry: 3.6271 },
        'FCEL': { qty: 97, entry: 4.05 }
    };
    
    const cash = 8.48;
    let positionValue = 0;
    let totalPnL = 0;
    
    Object.keys(positions).forEach(symbol => {
        if (prices[symbol]) {
            const pos = positions[symbol];
            const marketValue = pos.qty * prices[symbol].price;
            const cost = pos.qty * pos.entry;
            positionValue += marketValue;
            totalPnL += (marketValue - cost);
        }
    });
    
    const portfolioValue = cash + positionValue;
    const portfolioReturn = (portfolioValue - 1000) / 1000 * 100;
    
    // Update portfolio cards
    const cards = document.querySelectorAll('.grid.grid-cols-2 .bg-white');
    if (cards[0]) {
        cards[0].querySelector('p.text-2xl').textContent = `$${portfolioValue.toFixed(2)}`;
        cards[0].querySelector('p.text-sm').textContent = `${portfolioReturn >= 0 ? '+' : ''}${portfolioReturn.toFixed(2)}%`;
    }
    if (cards[3]) {
        cards[3].querySelector('p.text-2xl').textContent = `${totalPnL >= 0 ? '+' : ''}$${totalPnL.toFixed(2)}`;
    }
}

function updateBenchmarks(prices) {
    if (!prices.IWM || !prices.SPY) return;
    
    const investedAmount = 970.67;
    const iwmShares = 4.406; // Shares bought at $220.27
    const spyShares = 1.527; // Shares bought at $635.91
    
    const iwmValue = iwmShares * prices.IWM.price;
    const spyValue = spyShares * prices.SPY.price;
    
    const iwmGain = iwmValue - investedAmount;
    const spyGain = spyValue - investedAmount;
    
    const iwmReturn = (iwmGain / investedAmount) * 100;
    const spyReturn = (spyGain / investedAmount) * 100;
    
    // Update IWM display
    document.getElementById('iwmValue').textContent = `$${iwmValue.toFixed(2)}`;
    document.getElementById('iwmGain').textContent = `${iwmGain >= 0 ? '+' : ''}$${Math.abs(iwmGain).toFixed(2)}`;
    document.getElementById('iwmReturn').textContent = `${iwmReturn >= 0 ? '+' : ''}${iwmReturn.toFixed(2)}%`;
    
    // Update SPY display
    document.getElementById('spyValue').textContent = `$${spyValue.toFixed(2)}`;
    document.getElementById('spyGain').textContent = `${spyGain >= 0 ? '+' : ''}$${Math.abs(spyGain).toFixed(2)}`;
    document.getElementById('spyReturn').textContent = `${spyReturn >= 0 ? '+' : ''}${spyReturn.toFixed(2)}%`;
    
    // Update performance comparison
    const portfolioReturn = ((document.querySelector('.grid.grid-cols-2 p.text-2xl').textContent.replace('$', '') - 1000) / 1000) * 100;
    
    const vsIwm = portfolioReturn - iwmReturn;
    const vsSpy = portfolioReturn - spyReturn;
    
    document.getElementById('vsIwm').textContent = vsIwm >= 0 ? 
        `Outperforming by +${vsIwm.toFixed(2)}%` : 
        `Underperforming by ${vsIwm.toFixed(2)}%`;
    document.getElementById('vsIwm').className = vsIwm >= 0 ? 
        'text-lg font-bold text-green-600' : 
        'text-lg font-bold text-red-600';
    
    document.getElementById('vsSpy').textContent = vsSpy >= 0 ? 
        `Outperforming by +${vsSpy.toFixed(2)}%` : 
        `Underperforming by ${vsSpy.toFixed(2)}%`;
    document.getElementById('vsSpy').className = vsSpy >= 0 ? 
        'text-lg font-bold text-green-600' : 
        'text-lg font-bold text-red-600';
}

function updateLastRefreshTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });
    
    // Add or update refresh indicator
    let refreshIndicator = document.getElementById('refresh-time');
    if (!refreshIndicator) {
        refreshIndicator = document.createElement('p');
        refreshIndicator.id = 'refresh-time';
        refreshIndicator.className = 'text-xs text-gray-500 mt-2';
        const header = document.querySelector('h1');
        header.parentNode.insertBefore(refreshIndicator, header.nextSibling);
    }
    refreshIndicator.textContent = `Last updated: ${timeString}`;
}

// NO AUTO-REFRESH - Manual updates only
// Initial load when page opens
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard ready - Click "Refresh Prices" to update');
});