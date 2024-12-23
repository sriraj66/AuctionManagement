export function createPlayerForm(teamNumber, onSubmit) {
    const form = document.createElement('div');
    form.className = 'player-form-modal';
    
    form.innerHTML = `
        <div class="player-form-content">
            <span class="close-form">&times;</span>
            <h3>Add Player</h3>
            <form id="playerForm">
                <div class="form-group">
                    <label>Player Name*</label>
                    <input type="text" name="playerName" required>
                </div>
                <div class="form-group">
                    <label>Category*</label>
                    <select name="category" required>
                        <option value="">Select Category</option>
                        <option value="Professional">Professional</option>
                        <option value="Amateur">Amateur</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Profile Image</label>
                    <input type="file" name="profileImage" accept="image/*">
                </div>
                <div class="form-group">
                    <label>MPL ID</label>
                    <input type="text" name="mplId">
                </div>
                <div class="form-group">
                    <label>Age*</label>
                    <input type="number" name="age" required min="15" max="50">
                </div>
                <div class="form-group">
                    <label>Village Name</label>
                    <input type="text" name="villageName">
                </div>
                <div class="form-group">
                    <label>Player Role*</label>
                    <select name="playerRole" required>
                        <option value="">Select Role</option>
                        <option value="Batsman">Batsman</option>
                        <option value="Bowler">Bowler</option>
                        <option value="All-Rounder">All-Rounder</option>
                        <option value="Wicket-Keeper">Wicket-Keeper</option>
                    </select>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Total Matches</label>
                        <input type="number" name="totalMatches" min="0">
                    </div>
                    <div class="form-group">
                        <label>Matches Bowled</label>
                        <input type="number" name="matchesBowled" min="0">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Batting Runs</label>
                        <input type="number" name="battingRuns" min="0">
                    </div>
                    <div class="form-group">
                        <label>High Score</label>
                        <input type="number" name="highScore" min="0">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>30s</label>
                        <input type="number" name="thirties" min="0">
                    </div>
                    <div class="form-group">
                        <label>50s</label>
                        <input type="number" name="fifties" min="0">
                    </div>
                    <div class="form-group">
                        <label>100s</label>
                        <input type="number" name="hundreds" min="0">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Total Wickets</label>
                        <input type="number" name="totalWickets" min="0">
                    </div>
                    <div class="form-group">
                        <label>Economy</label>
                        <input type="number" name="economy" min="0" step="0.01">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Maiden Overs</label>
                        <input type="number" name="maidenOvers" min="0">
                    </div>
                    <div class="form-group">
                        <label>Hat-tricks</label>
                        <input type="number" name="hatTricks" min="0">
                    </div>
                </div>
                <button type="submit" class="submit-btn">Add Player</button>
            </form>
        </div>
    `;

    const closeBtn = form.querySelector('.close-form');
    closeBtn.onclick = () => form.remove();

    const playerForm = form.querySelector('#playerForm');
    playerForm.onsubmit = (e) => {
        e.preventDefault();
        const formData = new FormData(playerForm);
        const playerData = Object.fromEntries(formData);
        onSubmit(playerData, teamNumber);
        form.remove();
    };

    return form;
}