// 球員 ID（Kristaps Porzingis）
const PLAYER_NAME = 'Kristaps Porzingis';
const API_BASE = 'https://api.balldontlie.io/api/v1';

// ✅ 你的 API Key
const API_KEY = 'd20ba6d2-5739-4a35-aa5c-2f309f6930a6';

// 載入數據
document.addEventListener('DOMContentLoaded', function() {
    loadPlayerData();
});

// 主函數 - 獲取球員數據
async function loadPlayerData() {
    try {
        // 1. 先搵球員 ID
        const playerId = await getPlayerId(PLAYER_NAME);
        if (!playerId) {
            console.error('找不到球員');
            loadFallbackData();
            return;
        }

        // 2. 獲取球員統計
        const stats = await getPlayerStats(playerId);
        
        // 3. 獲取最近比賽
        const recentGames = await getRecentGames(playerId);

        // 4. 顯示數據
        displayStats(stats);
        displayRecentGames(recentGames);

    } catch (error) {
        console.error('API 載入失敗:', error);
        loadFallbackData(); // 如果 API 失敗，用備份數據
    }
}

// 搵球員 ID
async function getPlayerId(playerName) {
    try {
        const response = await fetch(`${API_BASE}/players?search=${playerName}&token=${API_KEY}`);
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            return data.data[0].id;
        }
        return null;
    } catch (error) {
        console.error('搵球員失敗:', error);
        return null;
    }
}

// 獲取球員季節統計
async function getPlayerStats(playerId) {
    try {
        const response = await fetch(`${API_BASE}/season_averages?player_ids[]=${playerId}&token=${API_KEY}`);
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            return data.data;
        }
        return [];
    } catch (error) {
        console.error('獲取統計失敗:', error);
        return [];
    }
}

// 獲取最近比賽
async function getRecentGames(playerId) {
    try {
        const response = await fetch(`${API_BASE}/games?player_ids[]=${playerId}&per_page=10&token=${API_KEY}`);
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            return data.data;
        }
        return [];
    } catch (error) {
        console.error('獲取比賽失敗:', error);
        return [];
    }
}

// 顯示季節統計
function displayStats(stats) {
    const tbody = document.getElementById('stats-body');
    tbody.innerHTML = '';
    
    if (stats.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No data available</td></tr>';
        return;
    }

    stats.reverse().forEach(season => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${season.season}</td>
            <td>${season.team?.name || 'N/A'}</td>
            <td>${season.games_played}</td>
            <td>${season.pts ? season.pts.toFixed(1) : 'N/A'}</td>
            <td>${season.pts && season.games_played ? (season.pts * season.games_played).toFixed(0) : 'N/A'}</td>
        `;
        tbody.appendChild(row);
    });
}

// 顯示最近比賽
function displayRecentGames(games) {
    const container = document.getElementById('recent-games');
    container.innerHTML = '';
    
    if (games.length === 0) {
        container.innerHTML = '<p style="text-align:center; padding: 20px;">No recent games data</p>';
        return;
    }

    games.slice(0, 6).forEach(game => {
        const card = document.createElement('div');
        card.className = 'game-card';
        
        const date = new Date(game.date).toLocaleDateString('en-US');
        const opponent = game.home_team.name === 'Boston Celtics' ? game.away_team.name : game.home_team.name;
        const points = game.player_ids?.includes(game.id) ? game.points : 'N/A';
        
        card.innerHTML = `
            <div class="date">${date}</div>
            <div class="score">${points}</div>
            <div class="opponent">vs ${opponent}</div>
        `;
        container.appendChild(card);
    });
}

// 備用數據（API 失敗時用）
function loadFallbackData() {
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            displayStats(formatFallbackStats(data.seasons));
            displayRecentGames(formatFallbackGames(data.recentGames));
        })
        .catch(error => console.error('備用數據載入失敗:', error));
}

// 格式化備用統計
function formatFallbackStats(seasons) {
    return seasons.map(s => ({
        season: parseInt(s.year.split('-')[0]),
        team: { name: s.team },
        games_played: s.games,
        pts: s.ppg
    }));
}

// 格式化備用比賽
function formatFallbackGames(games) {
    return games.map(g => ({
        date: g.date,
        home_team: { name: g.opponent },
        away_team: { name: 'Boston Celtics' },
        points: g.points
    }));
}
