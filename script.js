// 載入數據並顯示
document.addEventListener('DOMContentLoaded', function() {
    // 從 data.json 讀取數據
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            displayStats(data);
            displayRecentGames(data);
        })
        .catch(error => console.error('載入數據失敗:', error));
});

// 顯示統計表格
function displayStats(data) {
    const tbody = document.getElementById('stats-body');
    tbody.innerHTML = '';
    
    data.seasons.forEach(season => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${season.year}</td>
            <td>${season.team}</td>
            <td>${season.games}</td>
            <td>${season.ppg.toFixed(1)}</td>
            <td>${season.total}</td>
        `;
        tbody.appendChild(row);
    });
}

// 顯示最近得分
function displayRecentGames(data) {
    const container = document.getElementById('recent-games');
    container.innerHTML = '';
    
    data.recentGames.slice(0, 6).forEach(game => {
        const card = document.createElement('div');
        card.className = 'game-card';
        card.innerHTML = `
            <div class="date">${game.date}</div>
            <div class="score">${game.points}</div>
            <div class="opponent">vs ${game.opponent}</div>
        `;
        container.appendChild(card);
    });
}
