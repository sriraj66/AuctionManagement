import { validateTeamSize } from './validation.js';
import { showPopup } from './notifications.js';

// Player management functions
export function addPlayer(teamNumber) {
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

export function updatePlayerCount(teamNumber) {
    const teamPlayers = document.getElementById(`team${teamNumber}Players`);
    const countDisplay = document.getElementById(`team${teamNumber}Count`);
    countDisplay.textContent = `Players: ${teamPlayers.children.length}/18`;
}