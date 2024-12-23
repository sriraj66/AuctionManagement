import { validateMatchStart } from './validation.js';
import { showPopup } from './notifications.js';
import { closeModal } from './modal.js';

let matchData = null;

export function setupTeamsDisplay() {
    window.saveMatch = saveMatch;
}

function saveMatch() {
    const team1Name = document.getElementById('team1Name').value;
    const team2Name = document.getElementById('team2Name').value;
    
    const team1Players = Array.from(document.getElementById('team1Players').getElementsByTagName('input'))
        .map(input => input.value)
        .filter(name => name.trim() !== '');
    
    const team2Players = Array.from(document.getElementById('team2Players').getElementsByTagName('input'))
        .map(input => input.value)
        .filter(name => name.trim() !== '');
    
    const validation = validateMatchStart(team1Name, team2Name, team1Players, team2Players);
    if (!validation.valid) {
        showPopup(validation.message);
        return;
    }
    
    matchData = {
        team1: {
            name: team1Name,
            players: team1Players
        },
        team2: {
            name: team2Name,
            players: team2Players
        }
    };
    
    updateTeamsDisplay();
    updateTossSelect();
    closeModal();
    showPopup('Match setup saved successfully!');
}

function updateTeamsDisplay() {
    if (!matchData) return;

    const teamsDisplay = document.getElementById('teamsDisplay');
    teamsDisplay.innerHTML = '';

    const createTeamCard = (team) => {
        const card = document.createElement('div');
        card.className = 'team-card';
        
        card.innerHTML = `
            <h3>${team.name}</h3>
            <ul class="player-list">
                ${team.players.map(player => `<li>${player}</li>`).join('')}
            </ul>
        `;
        
        return card;
    };

    teamsDisplay.appendChild(createTeamCard(matchData.team1));
    teamsDisplay.appendChild(createTeamCard(matchData.team2));
}

function updateTossSelect() {
    if (!matchData) return;

    const tossSelect = document.getElementById('tossWinner');
    tossSelect.innerHTML = `
        <option value="">Select Team</option>
        <option value="team1">${matchData.team1.name}</option>
        <option value="team2">${matchData.team2.name}</option>
    `;
}