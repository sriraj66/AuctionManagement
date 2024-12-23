import { createPlayerForm } from './components/playerForm.js';
import { createPlayerTable } from './components/playerTable.js';
import { getTeams, addPlayer, removePlayer, setTeamName } from './state/teamState.js';
import { showPopup } from './notifications.js';
import { updateBoardsDisplay } from './boardsDisplay.js';

let modal;

export function setupModal() {
    modal = document.getElementById('matchSetupModal');
    const btn = document.getElementById('createMatchBtn');
    const span = document.getElementsByClassName('close-btn')[0];
    const tossSection = document.querySelector('.toss-section');
    const tossSelect = document.getElementById('tossWinner');

    // Hide toss section initially
    tossSection.style.display = 'none';

    // Set up team name input handlers
    ['team1', 'team2'].forEach(team => {
        const input = document.getElementById(`${team}Name`);
        input.onchange = (e) => {
            setTeamName(team.slice(-1), e.target.value);
            updatePlayerTables();
        };
    });

    // Set up Add Player button handlers
    const addPlayerButtons = document.querySelectorAll('.add-player-btn');
    addPlayerButtons.forEach(button => {
        const teamNumber = button.closest('.team').id.slice(-1);
        button.onclick = () => {
            try {
                const teams = getTeams();
                const team = `team${teamNumber}`;
                if (teams[team].players.length >= 18) {
                    showPopup('Maximum 18 players allowed per team!');
                    return;
                }

                const form = createPlayerForm(teamNumber, (playerData, teamNum) => {
                    addPlayer(teamNum, playerData);
                    updatePlayerTables();
                    updatePlayerCount(teamNum);
                    showPopup('Player added successfully!');
                });
                document.body.appendChild(form);
            } catch (error) {
                showPopup(error.message);
            }
        };
    });

    // Set up toss winner select handler
    tossSelect.addEventListener('change', (e) => {
        const selectedTeam = e.target.value;
        if (selectedTeam) {
            const teams = getTeams();
            showPopup(`${teams[selectedTeam].name} won the toss!`);
        }
    });

    btn.onclick = () => openModal();
    span.onclick = () => closeModal();
    window.onclick = (event) => {
        if (event.target === modal) {
            closeModal();
        }
    };

    window.saveMatch = saveMatch;
}

function updatePlayerCount(teamNumber) {
    const countDisplay = document.getElementById(`team${teamNumber}Count`);
    const teams = getTeams();
    const playerCount = teams[`team${teamNumber}`].players.length;
    countDisplay.textContent = `Players: ${playerCount}/18`;
}

function updatePlayerTables() {
    const teams = getTeams();
    ['team1', 'team2'].forEach(team => {
        const teamNumber = team.slice(-1);
        const container = document.getElementById(`${team}Players`);
        container.innerHTML = '';
        
        if (teams[team].players.length > 0) {
            const table = createPlayerTable(teams[team].players, (playerIndex) => {
                removePlayer(teamNumber, playerIndex);
                updatePlayerTables();
                updatePlayerCount(teamNumber);
                showPopup('Player removed successfully!');
            });
            container.appendChild(table);
        }
    });

    updateBoardsDisplay();
}

export function openModal() {
    if (modal) modal.style.display = 'block';
}

export function closeModal() {
    if (modal) modal.style.display = 'none';
}

function saveMatch() {
    const teams = getTeams();
    if (!teams.team1.name || !teams.team2.name) {
        showPopup('Please enter names for both teams!');
        return;
    }
    if (teams.team1.players.length === 0 || teams.team2.players.length === 0) {
        showPopup('Each team must have at least one player!');
        return;
    }

    // Show toss section and update select options
    const tossSection = document.querySelector('.toss-section');
    tossSection.style.display = 'block';
    const tossSelect = document.getElementById('tossWinner');
    tossSelect.innerHTML = `
        <option value="">Select Team</option>
        <option value="team1">${teams.team1.name}</option>
        <option value="team2">${teams.team2.name}</option>
    `;

    document.getElementById('matchSetupModal').style.display = 'none';
    updateBoardsDisplay();
    showPopup('Match setup saved successfully!');
}