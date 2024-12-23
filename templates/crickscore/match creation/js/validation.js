export function validateTeamSize(teamPlayers) {
    const MAX_PLAYERS = 18;
    return teamPlayers.children.length < MAX_PLAYERS;
}

export function validateMatchStart(team1Name, team2Name, team1Players, team2Players) {
    if (!team1Name || !team2Name) {
        return { valid: false, message: 'Please enter names for both teams!' };
    }
    
    if (team1Players.length === 0 || team2Players.length === 0) {
        return { valid: false, message: 'Each team must have at least one player!' };
    }

    return { valid: true };
}