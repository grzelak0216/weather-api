
function setDefaultDates() {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    document.getElementById('endDate').valueAsDate = yesterday;
    
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    document.getElementById('startDate').valueAsDate = weekAgo;
}

async function fetchWeatherData() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const resultDiv = document.getElementById('result');
    const fetchBtn = document.getElementById('fetchBtn');
    
    if (!startDate) {
        resultDiv.innerHTML = '<div class="error">Please select a start date</div>';
        return;
    }
    
    fetchBtn.disabled = true;
    resultDiv.innerHTML = '<div class="loading">Loading weather data...</div>';
    
    try {
        let url = `/api/v1/cities-scores?start_date=${startDate}`;
        if (endDate) {
            url += `&end_date=${endDate}`;
        }
        
        const response = await fetch(url);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch data');
        }
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    } finally {
        fetchBtn.disabled = false;
    }
}

function getScoreClass(score) {
    if (score >= 7) return 'score-high';
    if (score >= 4) return 'score-medium';
    return 'score-low';
}

function displayResults(data) {
    const { cities } = data;
    const resultDiv = document.getElementById('result');
    
    if (!cities || cities.length === 0) {
        resultDiv.innerHTML = '<div class="loading">No data available for selected dates</div>';
        return;
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>City</th>
                    <th>Country</th>
                    <th>Temperature (°C)</th>
                    <th>Wind Speed (km/h)</th>
                    <th>Humidity (%)</th>
                    <th>Cloud Cover (%)</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    cities.forEach((city, index) => {
        const scoreClass = getScoreClass(city.score);
        const rankClass = index === 0 ? 'best-score' : '';
        
        html += `
            <tr class="${rankClass}">
                <td>${index + 1}</td>
                <td>${city.city}</td>
                <td>${city.country}</td>
                <td>${city.temperature}</td>
                <td>${city.wind_speed}</td>
                <td>${city.relative_humidity}</td>
                <td>${city.cloud_cover}</td>
                <td><span class="score-badge ${scoreClass}">${city.score}</span></td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    
    resultDiv.innerHTML = html;
}

window.addEventListener('DOMContentLoaded', () => {
    setDefaultDates();
    fetchWeatherData();
});