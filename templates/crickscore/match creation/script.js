import { validateTeamSize, validateMatchStart } from './js/validation.js';
import { showPopup } from './js/notifications.js';

function addPlayer(teamNumber) {
    const teamPlayers = document.getElementById(`team${teamNumber}Players`);
    
    if (!validateTeamSize(teamPlayers)) {
        showPopup('Maximum 18 players allowed per team!');
        return;
    }
    
    const playerDiv = document.createElement('div');
    playerDiv.className = 'player';
    
    const playerInput = document.createElement('input');
    playerInput.type = 'text';
    playerInput.placeholder = 'Enter player name';
    
    const removeButton = document.createElement('button');
    removeButton.className = 'remove-player-btn';
    removeButton.innerHTML = '×';
    removeButton.onclick = () => {
        playerDiv.remove();
        updatePlayerCount(teamNumber);
    };
    
    playerDiv.appendChild(playerInput);
    playerDiv.appendChild(removeButton);
    teamPlayers.appendChild(playerDiv);
    
    updatePlayerCount(teamNumber);
}

function updatePlayerCount(teamNumber) {
    const teamPlayers = document.getElementById(`team${teamNumber}Players`);
    const countDisplay = document.getElementById(`team${teamNumber}Count`);
    countDisplay.textContent = `Players: ${teamPlayers.children.length}/18`;
}

function startMatch() {
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
    
    const matchData = {
        team1: {
            name: team1Name,
            players: team1Players
        },
        team2: {
            name: team2Name,
            players: team2Players
        }
    };
    
    console.log('Match Data:', matchData);
    showPopup('Match is ready to start!');
}

// Make functions available globally
window.addPlayer = addPlayer;
window.startMatch = startMatch;