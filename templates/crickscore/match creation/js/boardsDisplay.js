import { createPlayerTable } from './components/playerTable.js';
import { getTeams } from './state/teamState.js';

export function updateBoardsDisplay() {
    const teams = getTeams();
    const teamsDisplay = document.getElementById('teamsDisplay');
    teamsDisplay.innerHTML = '';

    ['team1', 'team2'].forEach(team => {
        if (teams[team].name && teams[team].players.length > 0) {
            const card = document.createElement('div');
            card.className = 'team-card';
            card.innerHTML = `
                <h3>${teams[team].name}</h3>
                ${createPlayerTable(teams[team].players).outerHTML}
            `;
            teamsDisplay.appendChild(card);
        }
    });
}