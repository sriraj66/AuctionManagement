let teams = {
    team1: { name: '', players: [] },
    team2: { name: '', players: [] }
};

export function getTeams() {
    return teams;
}

export function addPlayer(teamNumber, playerData) {
    const team = `team${teamNumber}`;
    if (teams[team].players.length >= 18) {
        throw new Error('Maximum 18 players allowed per team');
    }
    teams[team].players.push(playerData);
}

export function removePlayer(teamNumber, playerIndex) {
    const team = `team${teamNumber}`;
    teams[team].players.splice(playerIndex, 1);
}

export function setTeamName(teamNumber, name) {
    const team = `team${teamNumber}`;
    teams[team].name = name;
}

export function resetTeams() {
    teams = {
        team1: { name: '', players: [] },
        team2: { name: '', players: [] }
    };
}